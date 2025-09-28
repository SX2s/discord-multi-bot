import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio
import os
import random

# ---------------- SETTINGS ----------------
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Remove default help so we can use our custom one
bot.remove_command("help")

# FFmpeg local path
FFMPEG_PATH = os.path.join(os.path.dirname(__file__), "ffmpeg.exe")

# ---------------- YTDL CONFIG ----------------
youtube_dl.utils.bug_reports_message = lambda *args, **kwargs: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
}

ffmpeg_options = {'options': '-vn'}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, executable=FFMPEG_PATH, **ffmpeg_options), data=data)


# ---------------- EVENTS ----------------
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")


@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="general")
    if channel:
        await channel.send(f"👋 Welcome {member.mention} to {member.guild.name}!")
    role = discord.utils.get(member.guild.roles, name="Member")
    if role:
        await member.add_roles(role)


# ---------------- MODERATION ----------------
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member} was kicked. Reason: {reason}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member} was banned. Reason: {reason}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f"🧹 Deleted {amount} messages.", delete_after=5)

warns = {}
@bot.command()
async def warn(ctx, member: discord.Member, *, reason="No reason"):
    warns[member.id] = warns.get(member.id, 0) + 1
    await ctx.send(f"⚠️ {member.mention} warned ({warns[member.id]}). Reason: {reason}")
    if warns[member.id] >= 3:
        await member.kick(reason="3 warnings")
        await ctx.send(f"❌ {member} was kicked for 3 warnings.")


# ---------------- FUN COMMANDS ----------------
@bot.command()
async def joke(ctx):
    jokes = [
        "Why do Python programmers wear glasses? Because they can't C!",
        "I told my computer I needed a break, and it said 'No problem — I’ll go to sleep.'"
    ]
    await ctx.send(random.choice(jokes))

@bot.command()
async def quote(ctx):
    quotes = [
        "Code is like humor. When you have to explain it, it’s bad.",
        "First, solve the problem. Then, write the code."
    ]
    await ctx.send(random.choice(quotes))


# ---------------- INFO COMMANDS ----------------
@bot.command()
async def serverinfo(ctx):
    embed = discord.Embed(title="Server Info", color=discord.Color.blue())
    embed.add_field(name="Name", value=ctx.guild.name, inline=False)
    embed.add_field(name="Members", value=ctx.guild.member_count, inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"User Info - {member}", color=discord.Color.green())
    embed.add_field(name="ID", value=member.id, inline=False)
    embed.add_field(name="Joined", value=member.joined_at.strftime("%b %d %Y"), inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="Bot Info", description="Multi-purpose bot", color=discord.Color.purple())
    embed.add_field(name="Author", value="SX2", inline=False)
    await ctx.send(embed=embed)


# ---------------- MUSIC COMMANDS ----------------
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()
        await ctx.send(f"🎶 Joined {ctx.author.voice.channel}")
    else:
        await ctx.send("❌ Join a voice channel first.")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Left the channel.")
    else:
        await ctx.send("❌ Not in a channel.")

@bot.command()
async def play(ctx, *, query):
    if not ctx.author.voice:
        return await ctx.send("❌ You need to be in a voice channel.")
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()

    async with ctx.typing():
        player = await YTDLSource.from_url(query, loop=bot.loop, stream=True)
        ctx.voice_client.stop()
        ctx.voice_client.play(player, after=lambda e: print(f"Error: {e}") if e else None)
    await ctx.send(f"🎵 Now playing: **{player.title}**")

@bot.command()
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("⏸️ Paused")

@bot.command()
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("▶️ Resumed")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.send("⏹️ Stopped")


# ---------------- HELP COMMAND ----------------
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Help Menu", color=discord.Color.gold())
    embed.add_field(name="🎵 Music", value="!join, !leave, !play <song>, !pause, !resume, !stop", inline=False)
    embed.add_field(name="🛡️ Moderation", value="!kick, !ban, !warn, !clear", inline=False)
    embed.add_field(name="🎉 Fun", value="!joke, !quote", inline=False)
    embed.add_field(name="ℹ️ Info", value="!serverinfo, !userinfo, !info", inline=False)
    await ctx.send(embed=embed)



# Run bot with your token
# Load token from file
with open("token.txt", "r") as f:
    TOKEN = f.read().strip()

bot.run(TOKEN)
