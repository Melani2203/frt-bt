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

    )

    await ctx.send(embed=embed, view=BotonCalendario())

# Preguntas frecuentes **************************************
# ===== SELECT DE PREGUNTAS =====
class PreguntaDetalleSelect(discord.ui.Select):
    def __init__(self, categoria):
        self.categoria = categoria

        if categoria == "inscripciones":
            options = [
                discord.SelectOption(label="¿Cuándo son las inscripciones?"),
                discord.SelectOption(label="¿Cómo me anoto?"),
            ]

        elif categoria == "examenes":
            options = [
                discord.SelectOption(label="¿Qué materias hay en cada mesa?"),
                discord.SelectOption(label="¿Cómo recupero un parcial?"),
            ]

        elif categoria == "cursado":
            options = [
                discord.SelectOption(label="¿Cómo son los horarios?"),
                discord.SelectOption(label="¿Hay asistencia obligatoria?"),
            ]

        elif categoria == "presentacion_notas":
            options = [
                discord.SelectOption(label="¿Qué es la 5.3.1 y cómo pedir la excepción?"),
                discord.SelectOption(label="¿Cómo inscribirme fuera de término?"),
                discord.SelectOption(label="¿Cómo cambiarme de comisión?"),
            ]

        super().__init__(
            placeholder="Seleccioná una pregunta...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        respuesta = ""

        if self.values[0] == "¿Cuándo son las inscripciones?":
            respuesta = "Las inscripciones se realizan según el calendario académico."

        elif self.values[0] == "¿Cómo me anoto?":
            respuesta = "Debés ingresar al sistema Sysacad y seleccionar las materias."

        elif self.values[0] == "¿Qué materias hay en cada mesa?":
            respuesta = "Las materias disponibles se publican en cada turno de examen según la carrera."

        elif self.values[0] == "¿Cómo recupero un parcial?":
            respuesta = "Podés rendir recuperatorio en las fechas establecidas por la cátedra."

        elif self.values[0] == "¿Cómo son los horarios?":
            respuesta = "Se publican al inicio de cada cuatrimestre."

        elif self.values[0] == "¿Hay asistencia obligatoria?":
            respuesta = "Sí, generalmente se exige un porcentaje mínimo de asistencia."

        elif self.values[0] == "¿Qué es la 5.3.1 y cómo pedir la excepción?":
            respuesta = """**📌 Requisitos:**
Para pedir la excepción al art. 5.3.1 debés estar cursando las últimas materias de la carrera y no tener superposición entre horarios.

**📝 Procedimiento:**
Tenés que confeccionar una nota (ver modelo en Secretaría de Asuntos Estudiantiles) y presentarla en Mesa de Entrada.
Luego deberá ser tratada por el Consejo Directivo.
Finalmente podés consultar la respuesta en Dpto. Alumnos.

**📖 Art. 5.3.1:**
“Cuando al alumno le faltare para terminar de cursar su carrera, un número de asignaturas cuya carga horaria no supere el equivalente del último año de cursado de la misma...”
"""

        elif self.values[0] == "¿Cómo inscribirme fuera de término?":
            respuesta = """Debés presentar una nota en Mesa de Entrada explicando el motivo.

Luego:
• Será evaluada por las autoridades correspondientes  
• Puede ser aprobada o rechazada  

Se recomienda hacerlo lo antes posible."""

        elif self.values[0] == "¿Cómo cambiarme de comisión?":
            respuesta = """Para cambiarte de comisión:

• Consultá disponibilidad en otras comisiones  
• Presentá una solicitud (nota o sistema, según corresponda)  
• Esperá la aprobación del departamento o docente  

No siempre está garantizado el cambio."""

        embed = discord.Embed(
            title=self.values[0],
            description=respuesta,
            color=discord.Color.green()
        )

        await interaction.response.edit_message(embed=embed, view=self.view)


# ===== BOTÓN VOLVER =====
class VolverButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="⬅️ Volver", style=discord.ButtonStyle.secondary)

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="❓ Preguntas Frecuentes",
            description="Seleccioná una categoría 👇",
            color=discord.Color.red()
        )

        await interaction.response.edit_message(
            embed=embed,
            view=PreguntasView()
        )


# ===== VIEW DE PREGUNTAS =====
class PreguntaDetalleView(discord.ui.View):
    def __init__(self, categoria):
        super().__init__()
        self.add_item(PreguntaDetalleSelect(categoria))
        self.add_item(VolverButton())


# ===== SELECT DE CATEGORÍAS =====
class PreguntasSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="📚 Inscripciones"),
            discord.SelectOption(label="📝 Exámenes"),
            discord.SelectOption(label="🏫 Cursado"),
            discord.SelectOption(label="📄 Presentación de notas"),  # 👈 NUEVA
        ]

        super().__init__(
            placeholder="Seleccioná una categoría...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        categoria = ""

        if "Inscripciones" in self.values[0]:
            categoria = "inscripciones"

        elif "Exámenes" in self.values[0]:
            categoria = "examenes"

        elif "Cursado" in self.values[0]:
            categoria = "cursado"

        elif "Presentación" in self.values[0]:
            categoria = "presentacion_notas"

        embed = discord.Embed(
            title=self.values[0],
            description="Seleccioná una pregunta 👇",
            color=discord.Color.blue()
        )

        await interaction.response.edit_message(
            embed=embed,
            view=PreguntaDetalleView(categoria)
        )


# ===== VIEW PRINCIPAL =====
class PreguntasView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(PreguntasSelect())


# ===== COMANDO =====
@bot.command()
async def preguntas(ctx):
    embed = discord.Embed(
        title="❓ Preguntas Frecuentes",
        description="Seleccioná una categoría 👇",
        color=discord.Color.red()
    )

    await ctx.send(embed=embed, view=PreguntasView())
# **************************************

# Ejecutar
bot.run(TOKEN)
