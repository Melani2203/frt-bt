import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Cargar token
TOKEN = os.environ.get("DISCORD_TOKEN")

print("TOKEN:", TOKEN)

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

# Comando ,calendario26
class BotonCalendario(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(discord.ui.Button(
            label="📥 Descargar calendario",
            url="https://raw.githubusercontent.com/Melani2203/archivos-bot/main/CA2026.pdf"
        ))

@bot.command()
async def calendario26(ctx):
    embed = discord.Embed(
        description="# 📅 Calendario Académico\n\n"
                    "Podés descargar el calendario usando el botón de abajo 👇\n\n"
                    "También podés consultarlo en la página oficial de la facultad:\n"
                    "🔗 https://frt.utn.edu.ar/ \n"
                    "o en: https://frt.utn.edu.ar/wp-content/uploads/2025/11/CALENDARIO-ACADEMICO-2026.-Resol.-2394.pdf",
        color=discord.Color.orange()

        print("COMANDO EJECUTADO")
    )

    await ctx.send(embed=embed, view=BotonCalendario())

    # Preguntas frecuentes **************************************
class PreguntasSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="📚 Inscripciones", description="Fechas y requisitos"),
            discord.SelectOption(label="📝 Exámenes", description="Parciales e integrales"),
            discord.SelectOption(label="🏫 Cursado", description="Horarios y materias"),
        ]

        super().__init__(
            placeholder="Seleccioná una categoría...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "📚 Inscripciones":
            embed = discord.Embed(
                title="📚 Inscripciones",
                description="• ¿Cuándo son las inscripciones?\n• ¿Cómo me anoto?\n• Requisitos necesarios",
                color=discord.Color.blue()
            )

        elif self.values[0] == "📝 Exámenes":
            embed = discord.Embed(
                title="📝 Exámenes",
                description="• ¿Qué es un integral?\n• Fechas de parciales\n• Cómo recuperar",
                color=discord.Color.green()
            )

        elif self.values[0] == "🏫 Cursado":
            embed = discord.Embed(
                title="🏫 Cursado",
                description="• Horarios\n• Modalidad\n• Asistencia",
                color=discord.Color.orange()
            )

        await interaction.response.edit_message(embed=embed, view=self.view)

class PreguntasView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(PreguntasSelect())

@bot.command()
async def preguntas(ctx):
    embed = discord.Embed(
        title="❓ Preguntas Frecuentes",
        description="Seleccioná una categoría en el menú de abajo 👇",
        color=discord.Color.red()
    )

    await ctx.send(embed=embed, view=PreguntasView())

# **************************************

# Ejecutar
bot.run(TOKEN)
