import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Cargar token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents
intents = discord.Intents.default()
intents.message_content = True

# Prefijo de comandos (!)
bot = commands.Bot(command_prefix=",", intents=intents)

# Evento cuando el bot prende
@bot.event
async def on_ready():
    print(f"Conectado como {bot.user}")

# Comando ,ping
@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)

    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"{ctx.author.mention} Tu ping es **{latency}ms**",
        color=discord.Color.red()
    )

    await ctx.send(embed=embed)

# Comando ,calendario2026
@bot.command()
async def calendario2026(ctx):
    embed = discord.Embed(
        description="# Calendario Académico 2026 \n\n\n"
                    "Adjunto el calendario académico en PDF :point_up_2:.\n\n"
                    "También podés consultarlo en la página oficial de la facultad:\n"
                    "🔗 https://frt.utn.edu.ar/ \n"
                    "o en: https://frt.utn.edu.ar/wp-content/uploads/2025/11/CALENDARIO-ACADEMICO-2026.-Resol.-2394.pdf",
        color=discord.Color.orange()
    )

    file = discord.File("CA2026.pdf", filename="CA2026.pdf")

    await ctx.send(embed=embed, file=file)

# Ejecutar
bot.run(TOKEN)