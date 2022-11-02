import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

# OPCIONES DE VOZ / IDIOMA
id1 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0"
id2 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
id3 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0"
id4 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"


# ESCUCHAR NUESTRO MICROFONO Y DEVOLVER EL AUDIO COMO TEXTO
def tranformar_audio_en_texto():
    # ALMACENAR RECOGNIZER EN VARIABLE
    r = sr.Recognizer()

    # CONFIGURAR EL MICROFONO
    with sr.Microphone() as origen:

        # TIEMPO DE ESPERAR
        r.pause_threshold = 0.8

        # INFORMAR QUE COMENZO LA GRABACION
        print("Ya puedes hablar")

        # GUARDAR LO QUE ESCUCHE COMO AUDIO
        audio = r.listen(origen)

    try:
        # BUSCAR EN GOOGLE
        pedido = r.recognize_google(audio, language="es-pe")

        # PRUEBA DE QUE PUDO INGRESAR
        print("Digiste: " + pedido)

        # DEVOLVER A PEDIDO
        return pedido
    # EN CASO DE QUE NO COMPRENDA EL AUDIO
    except sr.UnknownValueError:

        # PRUEBA DE QUE NO COMPRENDIO EL AUDIO
        print("Ups, no entendi")

        # DEVOLVER ERROR
        return "sigo esperando"

    # EN CASO DE NO RESOLVER EL PEDIDO
    except sr.RequestError:

        # PRUEBA DE QUE NO COMPRENDIO EL AUDIO
        print("Ups, no hay servicio")

        # DEVOLVER ERROR
        return "sigo esperando"

    # ERROR INESPERADO
    except:

        # PRUEBA DE QUE NO COMPRENDIO EL AUDIO
        print("Ups, algo ha salido mal")

        # DEVOLVER ERROR
        return "sigo esperando"


# FUNCION PARA QUE EL ASISTENTE PUEDA SER ESCUCHADO
def hablar(mensaje):
    # ENCENDER EL MOTOR DE pyttsx3
    engine = pyttsx3.init()
    engine.setProperty("voice", id1)
    # pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


# INFORMAR EL DIA DE LA SEMANA
def pedir_dia():
    # CREAR VARIABLE CON DATOS DE HOY
    dia = datetime.date.today()
    print(dia)

    # CREAR UNA VARIABLE PARA EL DIA DE SEMANA
    dia_semana = dia.weekday()
    print(dia_semana)

    # DICCIONARIO CON NOMBRES DE DIAS
    calendario = {0: "Lunes",
                  1: "Martes",
                  2: "Miércoles",
                  3: "Jueves",
                  4: "Viernes",
                  5: "Sábado",
                  6: "Domingo"}

    # DECIR EL DIA DE LA SEMANA
    hablar(f"Hoy es {calendario[dia_semana]}")


# INFORMAR QUE HORA ES
def pedir_hora():
    # CREAR UNA VARIBLE CON DATOS DE LA HORA
    hora = datetime.datetime.now()
    hora = f"En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos"
    print(hora)

    # DECIR LA HORA
    hablar(hora)


# FUNCION SALUDO INICIAL
def saludo_inicial():
    # CREAR VARIABLE CON DATOS DE HORA
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = "Buenas noches"
    elif 6 <= hora.hour < 13:
        momento = "Buen dia"
    else:
        momento = "Buenas tardes"

    # DECIR EL SALUDO
    hablar(f"{momento}, soy Helena, tu asistente personal. Por favor, en que te puedo ayudar")


# FUNCION CENTRAL DEL ASSITENTE
def pedir_cosas():
    # ACTIVAR EL SALUDO INICIAL
    saludo_inicial()

    # VARIABLE DE CORTE
    comenzar = True

    # loop central
    while comenzar:

        # ACTIVAR EL MICRO Y GUARDA EL PEDIDO EN UN STRING
        pedido = tranformar_audio_en_texto().lower()

        if "abre youtube" in pedido:
            hablar("Con gusto, estoy abriendo youTube")
            webbrowser.open("https://www.youtube.com")
            continue
        elif "abre navegador" in pedido:
            hablar("Claro estoy en eso")
            webbrowser.open("https://www.google.com.pe")
            continue
        elif "qué día es hoy" in pedido:
            pedir_dia()
            continue
        elif "qué hora es" in pedido:
            pedir_hora()
            continue
        elif "busca en wikipedia" in pedido:
            hablar("Buscando eso en wikipedia")
            pedido = pedido.replace("busca en wikipedia", "")
            wikipedia.set_lang("es")
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar("wikipedia dice lo siguiente:")
            hablar(resultado)
            continue
        elif "busca en internet" in pedido:
            hablar("Ya mismo estoy en eso")
            pedido = pedido.replace("busca en internet", "")
            pywhatkit.search(pedido)
            hablar("Esto es lo que he encontrado")
            continue
        elif "reproducir" in pedido:
            hablar("Buena idea ya comienzo a reproducirlo")
            pywhatkit.playonyt(pedido)
            continue
        elif "chiste" in pedido:
            hablar(pyjokes.get_joke("es"))
            continue
        elif "precio de las acciones" in pedido:
            accion = pedido.split("de")[-1].strip()
            cartera = {"apple":"APPL",
                       "amazon":"AMZN",
                       "google":"GOOGL"}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info["regularMarketPrice"]
                hablar(f"La encontre, el precio de {accion} es {precio_actual}")
                continue
            except:
                hablar("Perdón pero no la he encontrado")
                continue
        elif "adiós" in pedido:
            hablar("Me voy a descansar, cualquier cosa me avisas")
            break

pedir_cosas()