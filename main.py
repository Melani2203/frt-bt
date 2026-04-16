import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
from google import genai

# =========================
# 🔑 CONFIG
# =========================
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GUILD_ID = 1361312541766058184

if not DISCORD_TOKEN:
    raise ValueError("❌ Falta DISCORD_TOKEN en Railway")

if not GEMINI_API_KEY:
    raise ValueError("❌ Falta GEMINI_API_KEY en Railway")

print("TOKEN cargado:", bool(DISCORD_TOKEN))
print("GEMINI cargado:", bool(GEMINI_API_KEY))

# =========================
# 🤖 IA
# =========================
client = genai.Client(api_key=GEMINI_API_KEY)

# =========================
# ⚙️ BOT
# =========================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=",", intents=intents)

# =========================
# 📄 REGLAMENTO
# =========================
def obtener_contenido_reglamento():
    try:
        with open("Reglamento-de-Estudios-Ord-1549.txt", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print("Error cargando reglamento:", e)
        return None

REGLAMENTO_TEXTO = obtener_contenido_reglamento()

# =========================
# 🚀 READY
# =========================
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

    try:
        guild = discord.Object(id=GUILD_ID)
       bot.tree.clear_commands(guild=guild)
        synced = await bot.tree.sync(guild=guild)
        
        print(f"🚀 Slash commands sincronizados en el servidor: {len(synced)}")
    except Exception as e:
        print(f"❌ Error durante la sincronización: {e}")

# =========================
# 📅 EMBED CALENDARIO
# =========================
def crear_embed_calendario():
    return discord.Embed(
        description="# 📅 Calendario Académico\n\n"
                    "Podés descargar el calendario usando el botón de abajo 👇\n\n"
                    "También podés consultarlo en el canal <#1361312542244344022> o en la página oficial de la facultad:\n"
                    "🔗 https://frt.utn.edu.ar/ \n"
                    "o en: https://frt.utn.edu.ar/wp-content/uploads/2025/11/CALENDARIO-ACADEMICO-2026.-Resol.-2394.pdf",
        color=discord.Color.orange()
    )

# =========================
# 🤖 COMANDO IA (/cr)
# =========================
@bot.tree.command(
    name="cr",
    description="Consultar reglamento con IA",
    guild=discord.Object(id=GUILD_ID)
)
@app_commands.describe(pregunta="Escribe tu duda")
async def cr_slash(interaction: discord.Interaction, pregunta: str):

    if not REGLAMENTO_TEXTO:
        await interaction.response.send_message(
            "❌ Reglamento no cargado",
            ephemeral=True
        )
        return

    await interaction.response.defer(thinking=True)

    try:
        REGLAMENTO_LIMITADO = REGLAMENTO_TEXTO[:12000]

        prompt = f"""
Sos un asistente de la UTN FRT.

Usá SOLO el reglamento.
Si no está, respondé: "No está especificado en el reglamento".
Sé claro y breve.

REGLAMENTO:
{REGLAMENTO_LIMITADO}

PREGUNTA:
{pregunta}
"""

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        # 🔥 Manejo robusto de respuesta
        texto = response.text if hasattr(response, "text") and response.text else None

        if not texto and hasattr(response, "candidates"):
            try:
                texto = response.candidates[0].content.parts[0].text
            except:
                texto = None

        if not texto:
            texto = "❌ No se pudo generar respuesta."

        await interaction.followup.send(texto[:2000])

    except Exception as e:
        print("Error IA:", e)
        await interaction.followup.send("❌ Error con la IA")


# =========================
# 💬 COMANDO PREFIJO ,cr
# =========================
@bot.command(name="cr")
async def cr_prefix(ctx, *, pregunta: str):

    if not REGLAMENTO_TEXTO:
        await ctx.send("❌ Reglamento no cargado")
        return

    async with ctx.typing():
        try:
            REGLAMENTO_LIMITADO = REGLAMENTO_TEXTO[:12000]

            prompt = f"""
Sos un asistente de la UTN FRT.

Usá SOLO el reglamento.
Si no está, respondé: "No está especificado en el reglamento".
Sé claro y breve.

REGLAMENTO:
{REGLAMENTO_LIMITADO}

PREGUNTA:
{pregunta}
"""

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

            # 🔥 Manejo robusto de respuesta
            texto = response.text if hasattr(response, "text") and response.text else None

            if not texto and hasattr(response, "candidates"):
                try:
                    texto = response.candidates[0].content.parts[0].text
                except:
                    texto = None

            if not texto:
                texto = "❌ No se pudo generar respuesta."

            await ctx.send(texto[:2000])

        except Exception as e:
            print("Error IA:", e)
            await ctx.send("❌ Error con la IA")
            
# =========================
# 📅 BOTÓN CALENDARIO
# =========================
class BotonCalendario(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # 👈 importante para que no expire

        self.add_item(discord.ui.Button(
            label="📥 Descargar calendario",
            url="https://raw.githubusercontent.com/Melani2203/archivos-bot/main/CA2026.pdf"
        ))

# =========================
# 📌 SLASH COMMAND
# =========================
@bot.tree.command(
    name="calendario26",
    description="Ver calendario académico 2026"
)
async def calendario26_slash(interaction: discord.Interaction):
    await interaction.response.send_message(
        embed=crear_embed_calendario(),
        view=BotonCalendario()
    )

# =========================
# 💬 PREFIX COMMAND
# =========================
@bot.command(name="calendario26")
async def calendario26_prefix(ctx):
    await ctx.send(
        embed=crear_embed_calendario(),
        view=BotonCalendario()
    )

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
# 📚 ROLES DE AÑO
# =========================
ROLES_AÑO = {
    "1": 1425540896035835987,
    "2": 1425541312626819072,
    "3": 1425541364208107531,
    "4": 1425541412262383657,
    "5": 1425541438497755198,
}

# =========================
# 📚 COMANDO PRINCIPAL
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

    await ctx.send(embed=embed, view=AñosView())


# =========================
# 🎛️ BOTONES DE AÑOS
# =========================
class AñosView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def manejar_año(self, interaction, año):
        guild = interaction.guild
        user = interaction.user
        rol = guild.get_role(ROLES_AÑO[año])

        # 🔴 SI YA TIENE EL ROL
        if rol in user.roles:
            await interaction.response.send_message(
                content=f"ℹ️ Ya posees el rol de {año}° año",
                view=ConfirmarAñoView(año, rol),
                ephemeral=True
            )
            return

        # 🟢 SI NO LO TIENE → LO AGREGA
        await user.add_roles(rol)

        embed = discord.Embed(
            description=obtener_materias(año),
            color=discord.Color.blue()
        )

        await interaction.response.send_message(
            content=f"✅ Se te asignó el rol de {año}° año",
            embed=embed,
            view=MateriasView(año),
            ephemeral=True
        )

    @discord.ui.button(label="1️⃣ 1er Año", style=discord.ButtonStyle.secondary)
    async def año1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.manejar_año(interaction, "1")

    @discord.ui.button(label="2️⃣ 2do Año", style=discord.ButtonStyle.secondary)
    async def año2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.manejar_año(interaction, "2")

    @discord.ui.button(label="3️⃣ 3er Año", style=discord.ButtonStyle.secondary)
    async def año3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.manejar_año(interaction, "3")

    @discord.ui.button(label="4️⃣ 4to Año", style=discord.ButtonStyle.secondary)
    async def año4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.manejar_año(interaction, "4")

    @discord.ui.button(label="5️⃣ 5to Año", style=discord.ButtonStyle.secondary)
    async def año5(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.manejar_año(interaction, "5")


# =========================
# VIEW CUANDO YA TIENE EL AÑO
# =========================
class ConfirmarAñoView(discord.ui.View):
    def __init__(self, año, rol):
        super().__init__(timeout=60)
        self.año = año
        self.rol = rol

    @discord.ui.button(label="➡️ Continuar a materias", style=discord.ButtonStyle.secondary)
    async def continuar(self, interaction: discord.Interaction, button: discord.ui.Button):

        embed = discord.Embed(
            description=obtener_materias(self.año),
            color=discord.Color.blue()
        )

        await interaction.response.send_message(
            embed=embed,
            view=MateriasView(self.año),
            ephemeral=True
        )

    @discord.ui.button(label="❌ Eliminar rol", style=discord.ButtonStyle.secondary)
    async def eliminar(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.user.remove_roles(self.rol)

        await interaction.response.send_message(
            f"❌ Se eliminó el rol de {self.año}° año",
            ephemeral=True
        )


# =========================
# 📝 TEXTO
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
# 🎯 ROLES DE MATERIAS
# =========================
ROLES = {
    "1": [
        ("🔢 Análisis I", 1425686379559653386),
        ("⚡ Física I", 1425686383216955413),
        ("📐 Álgebra", 1425686381602279545),
        ("🧠 Lógica", 1425686385771417641),
        ("⚙️ Sistemas", 1425686388401242225),
        ("💻 Algoritmos", 1425686386463473807),
        ("💾 Arquitectura", 1425686387243614278),
        ("🌍 Ingeniería", 1425686384860987433),
    ],
    "2": [
        ("🔢 Análisis II", 1425686389504344145),
        ("⚡ Física II", 1425686390024437811),
        ("📒 Inglés I", 1425686390615838820),
        ("📝 Sintaxis", 1425686391135670333),
        ("👨‍💻 Paradigmas", 1425686391613816923),
        ("💿 SO", 1425686391970463744),
        ("🧠 Análisis SI", 1425686392503144610),
    ],
    "3": [
        ("📒 Inglés II", 1425686813338501120),
        ("🎲 Probabilidad", 1425686395191693483),
        ("💰 Economía", 1425686396676472904),
        ("🗄️ BD", 1425686397183987712),
        ("💻 Desarrollo", 1425686397724917770),
        ("🌐 Comunicación", 1425686811719762071),
        ("📊 Numérico", 1425686812160036864),
        ("🖊️ Diseño", 1425686812709617736),
    ],
    "4": [
        ("⚖️ Legislación", 1425686813871177799),
        ("⚙️ Calidad", 1425688174801195028),
        ("🌐 Redes", 1425688175510159482),
        ("🔎 IO", 1425688176168800387),
        ("🎮 Simulación", 1425688176818786304),
        ("🤖 Automatización", 1425688178681057300),
        ("🖥️ Administración", 1425688181830975548),
    ],
    "5": [
        ("🧠 IA", 1425688182732624074),
        ("📊 Ciencia Datos", 1425688184045699123),
        ("🗃️ Gestión", 1425688447670157473),
        ("📈 Gerencial", 1425688449469382728),
        ("🛡️ Seguridad", 1425688451960930429),
        ("🧾 Proyecto", 1425688453949034579),
    ]
}


# =========================
# 🎛️ BOTONES DE MATERIAS
# =========================
class MateriasView(discord.ui.View):
    def __init__(self, año):
        super().__init__(timeout=None)

        for nombre, role_id in ROLES[año]:
            self.add_item(BotonMateria(nombre, role_id))


# =========================
# 🔘 BOTÓN INDIVIDUAL
# =========================
class BotonMateria(discord.ui.Button):
    def __init__(self, label, role_id):
        super().__init__(label=label, style=discord.ButtonStyle.secondary)
        self.role_id = role_id

    async def callback(self, interaction: discord.Interaction):
        role = interaction.guild.get_role(self.role_id)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(
                f"❌ Se te quitó el rol {role.name}",
                ephemeral=True
            )
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(
                f"✅ Se te asignó el rol {role.name}",
                ephemeral=True
            )

# =========================
# RUN
# =========================
bot.run(DISCORD_TOKEN)
