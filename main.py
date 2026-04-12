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

# Prefijo de comandos (,)
bot = commands.Bot(command_prefix=",", intents=intents)

# Evento cuando el bot prende
@bot.event
async def on_ready():
    print(f"Conectado como {bot.user}")

# ************************************** Comando ,calendario26 ************************************
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

# ******* BOTON SYSACAD *******
class BotonSysacad(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(discord.ui.Button(
            label="🌐 Ir a Sysacad",
            url="https://sysacad.frt.utn.edu.ar/"
        ))


# ********************* PREGUNTAS ************************
class PreguntaDetalleSelect(discord.ui.Select):
    def __init__(self, categoria):
        self.categoria = categoria
        options = []

        if categoria == "inscripciones":
            options = [
                discord.SelectOption(label="¿Cuándo son las inscripciones?"),
                discord.SelectOption(label="¿Cómo me anoto al cursado de una materia?"),
            ]

        elif categoria == "examenes finales":
            options = [
                discord.SelectOption(label="¿Qué materias hay en cada mesa de examen final?"),
                discord.SelectOption(label="¿Cuales son las fechas de examenes finales?"),
                discord.SelectOption(label="¿Cómo me anoto a un examen final?"),
                discord.SelectOption(label="¿Puedo rendir un examen final sin tener libreta universitaria?"),
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

        # ************************ INSCRIPCIONES ************************
        if self.values[0] == "¿Cuándo son las inscripciones?":
            respuesta = "Las inscripciones se realizan según el calendario académico. Lo pueden revisar con el comando **,calendario26** "

        elif self.values[0] == "¿Cómo me anoto al cursado de una materia?":
            respuesta = """Debés ingresar al sistema de autogestion de la facultad “Sysacad”. 
Podes hacerlo tocando el boton de abajo que te llevara directo a la pagina de autogestion. Si es la primera vez que ingresas tu usuario va a ser numero de lajago y tu contraseña tu DNI.
En que no te deje ingresar acercate por Secretaria de Asuntos Estudiantiles o Dpto. Alumnos para restablecer tu contraseña.
Una vez que ingreses entras a la seccion de inscripción al cursado y seleccionas las materias y comisiones en las que queres anotarte.
Si no te deja anotarte por ahi intenta nuevamente en los dias siguientes o llegate por Dpto. Alumnos para presentar una nota de Inscripcion fuera de termino/Ampliación de cupos."""

            embed = discord.Embed(
                title=self.values[0],
                description=respuesta,
                color=discord.Color.green()
            )

            embed.set_footer(text="Facultad Regional Tucumán")

            await interaction.response.edit_message(
                embed=embed,
                view=BotonSysacad()
            )
            return

        # ************************ EXAMENES ************************
        elif self.values[0] == "¿Qué materias hay en cada mesa de examen final?":
            respuesta = "Podes revisar que materias hay en cada mesa en . . ."

        elif self.values[0] == "¿Cuales son las fechas de examenes finales?":
            respuesta = "Podes revisar cuando son las mesas de examenes en el calendario academico usando el comando **,calendario26**"

        elif self.values[0] == "¿Cómo me anoto a un examen final?":
            respuesta = """Debés ingresar al sistema de autogestion de la facultad “Sysacad”. 
Podes hacerlo tocando el boton de abajo que te llevara directo a la pagina de autogestion. Si es la primera vez que ingresas tu usuario va a ser numero de lajago y tu contraseña tu DNI.
En que no te deje ingresar acercate por Secretaria de Asuntos Estudiantiles o Dpto. Alumnos para restablecer tu contraseña.
Una vez que ingreses entras a la seccion de inscripción a examenes y seleccionas las materias en las que queres anotarte.
Cualquier inconveniente podes llegar a consultar en Dpto. Legajos y Actas"""

            embed = discord.Embed(
                title=self.values[0],
                description=respuesta,
                color=discord.Color.green()
            )

            embed.set_footer(text="Facultad Regional Tucumán")

            await interaction.response.edit_message(
                embed=embed,
                view=BotonSysacad()
            )
            return

        elif self.values[0] == "¿Puedo rendir un examen final sin tener libreta universitaria?":
            respuesta = ""

        # ************************ CURSADO ************************
        elif self.values[0] == "¿Cómo son los horarios?":
            respuesta = "Se publican al inicio de cada cuatrimestre."

        elif self.values[0] == "¿Hay asistencia obligatoria?":
            respuesta = "Sí, generalmente se exige un porcentaje de mínimo 75% de asistencia."

        # ************************ PRESENTACION ************************
        elif self.values[0] == "¿Qué es la 5.3.1 y cómo pedir la excepción?":
            respuesta = """**📌 Requisitos:**
Para pedir la excepción al art. 5.3.1 debés estar cursando las últimas materias de la carrera y no tener superposición entre horarios.

**📝 Procedimiento:**
Tenés que confeccionar una nota (ver modelo en Secretaría de Asuntos Estudiantiles) y presentarla en Mesa de Entrada.
Luego deberás esperar que sea tratado por el Consejo Directivo quien definirá si se aprueba el pedido y se da curso para que sea tratado por Consejo Superior, o si rechaza el mismo.
Finalmente podés consultar la respuesta en Dpto. Alumnos.

**📖 Art. 5.3.1:**
“Cuando al alumno le faltare para terminar de cursar su carrera, un número de asignaturas cuya carga horaria no supere el equivalente del último año de cursado de la misma, no se aplicarán las exigencias del Régimen de Correlativas para el cursado; esta norma no lo exime de respetar el Régimen de Correlativas para rendir la evaluación final de las asignaturas cursadas en estas condiciones. En el caso que la carrera tenga en su último nivel un cuatrimestre, se tomará lo anterior o hasta (30) horas, según resulte el número mayor”.
"""

        elif self.values[0] == "¿Cómo inscribirme fuera de término?":
            respuesta = """Tenés que confeccionar una nota (busca el modelo de la nota por la Secretaría de Asuntos Estudiantiles) indicando el motivo por el cual no pudiste inscribirte en término, adjuntando documentación necesaria en el caso que corresponda. 
Presentás esta nota por Dpto. Mesa de Entrada y esperas que Secretaría Académica evalúe el pedido. Luego consultas la respuesta en el Dpto. Alumnos.     
Se recomienda hacerlo lo antes posible."""

        elif self.values[0] == "¿Cómo cambiarme de comisión?":
            respuesta = """Para cambiarte de comisión deben existir motivos de peso y documentados para pedir el cambio, como ser razones laborales u otras actividades comprobables.
Tenés que confeccionar nota pidiendo el cambio de comisión (busca el modelo de la nota por la Secretaría de Asuntos Estudiantiles), indicando el motivo y adjuntando la documentación necesaria, luego presentas la nota por Dpto. Mesa de Entrada y tenés que esperar que Secretaría Académica evalúe el pedido, luego consultas la respuesta en el Dpto. Alumnos. 
No siempre está garantizado el cambio."""

        embed = discord.Embed(
            title=self.values[0],
            description=respuesta,
            color=discord.Color.green()
        )

        embed.set_footer(text="Facultad Regional Tucumán")

        await interaction.response.edit_message(
            embed=embed,
            view=PreguntaDetalleView(self.categoria)
        )

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
# ******* BOTON SYSACAD *******
class BotonSysacad(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(discord.ui.Button(
            label="🌐 Ir a Sysacad",
            url="https://sysacad.frt.utn.edu.ar/"
        ))

# ===== VIEW DE PREGUNTAS =====
class PreguntaDetalleView(discord.ui.View):
    def __init__(self, categoria):
        super().__init__()
        self.add_item(PreguntaDetalleSelect(categoria))
        self.add_item(VolverButton())


# **************** CATEGORIAS ******************
class PreguntasSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="📚 Inscripciones"),
            discord.SelectOption(label="📝 Exámenes finales"),
            discord.SelectOption(label="🏫 Cursado"),
            discord.SelectOption(label="📄 Presentación de notas"),
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
            categoria = "examenes finales"

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

# =========================
# 📚 MATERIAS POR AÑO
# =========================
@bot.command()
async def materias(ctx):
    embed = discord.Embed(
        description="""**Selecciona en que años estas cursando** 
1️⃣╏1er Año  
2️⃣╏2do Año  
3️⃣╏3er Año  
4️⃣╏4to Año  
5️⃣╏5to Año""",
        color=discord.Color.green()
    )

    msg = await ctx.send(embed=embed)

    for emoji in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]:
        await msg.add_reaction(emoji)

# =========================
# DETECTAR REACCIONES
# =========================
@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    emoji = str(reaction.emoji)

    mapa = {
        "1️⃣": "1",
        "2️⃣": "2",
        "3️⃣": "3",
        "4️⃣": "4",
        "5️⃣": "5"
    }

    if emoji in mapa:
        año = mapa[emoji]

        await reaction.message.channel.send(
            f"{user.mention} seleccionaste {emoji}",
            view=AñoButtonView(año, user.id)
        )

# =========================
# BOTÓN INTERMEDIO (CLAVE)
# =========================
class AñoButtonView(discord.ui.View):
    def __init__(self, año, user_id):
        super().__init__(timeout=30)
        self.año = año
        self.user_id = user_id

    @discord.ui.button(label="Abrir materias", style=discord.ButtonStyle.primary)
    async def abrir(self, interaction: discord.Interaction, button: discord.ui.Button):

        # 🔒 Solo el usuario que reaccionó puede usarlo
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "❌ Este botón no es para vos.",
                ephemeral=True
            )
            return

        descripcion = obtener_materias(self.año)

        embed = discord.Embed(
            description=descripcion,
            color=discord.Color.blue()
        )

        await interaction.response.send_message(
            embed=embed,
            view=MateriasView(self.año),
            ephemeral=True
        )

# =========================
# MATERIAS TEXTO
# =========================
def obtener_materias(año):
    if año == "1":
        return """**1er año -Selecciona que materias estas cursando:** 
🔢╏análisis matemático ❘.
⚡╏física ❘.
📐╏álgebra y geometría analítica.
🧠╏lógica y estructuras discretas.
⚙️╏sistemas y procesos de negocios.
💻╏algoritmos y estructuras de datos.
💾╏arquitectura de computadoras.
🌍╏ingeniería y sociedad."""

    elif año == "2":
        return """**2do año - Selecciona que materias estas cursando:**
🔢╏análisis matemático ❘❘
⚡╏física ❘❘
📒╏inglés ❘
📝╏sintaxis y semántica de los lenguajes
👨‍💻╏paradigmas de programación
💿╏sistemas operativos
🧠╏análisis de sistemas de información"""

    elif año == "3":
        return """**3er año - Selecciona que materias estas cursando:** 
📒╏inglés ❘❘
🎲╏probabilidad y estadística
💰╏economía
🗄️╏bases de datos
💻╏desarrollo de software
🌐╏comunicación de datos
📊╏análisis numérico
🖊️╏diseño de sistemas de información"""

    elif año == "4":
        return """**4to año - Selecciona que materias estas cursando:**
⚖️╏legislación
⚙️╏ingeniería y calidad de software
🌐╏redes de datos
🔎╏investigación operativa
🎮╏simulación
🤖╏tecnologías para la automatización
🖥️╏administración de sistemas de información"""

    elif año == "5":
        return """**5to año - Selecciona que materias estas cursando:**
🧠╏inteligencia artificial
📊╏ciencia de datos
🗃️╏sistemas de gestión
📈╏gestión gerencial
🛡️╏seguridad en los sistemas de información
🧾╏proyecto final"""

# =========================
# BOTONES DE MATERIAS (BASE)
# =========================
class MateriasView(discord.ui.View):
    def __init__(self, año):
        super().__init__(timeout=None)
        self.año = año

    @discord.ui.button(label="Seleccionar materias", style=discord.ButtonStyle.success)
    async def seleccionar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "✅ Después acá podés asignar roles por materia.",
            ephemeral=True
        )

# =========================



# Ejecutar
bot.run(TOKEN)
