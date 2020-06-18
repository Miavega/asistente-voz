import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import smtplib
import webbrowser as wb
import os
import pyautogui
import psutil
import pyjokes

engine = pyttsx3.init()

voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[0].id)

wikipedia.set_lang("es")

#languages = ['en', 'de', 'es', 'gl', 'eu', 'it']
language = 'es'

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak(Time)

def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)

    speak(day)
    speak(month)
    speak(year)

def wishme():
    speak("Bienvenido de nuevo señor")

    speak("La hora actual es")
    time()

    speak("La fecha actual es")
    date()

    hour = datetime.datetime.now().hour

    if hour >= 6 and hour < 12:
        speak("Buenos días señor")
    elif hour >= 12 and hour < 18:
        speak("Buenas tardes señor")
    else:
        speak("Buenas noches")

    speak("Fatzi a tu servicio! Por favor dime cómo puedo ayudarte?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        r.pause_threshold = 1
        audio = r.listen(source)

        try:
            print("Reconociendo...")
            query = r.recognize_google(audio, language='es-ES')
            print(query)
        except Exception as e:
            print(e)
            speak("No pude entender, repítelo de nuevo por favor...")

            return "None"

    return query

def sendEmail(to, content):
    # para otros correos ver https://automatetheboringstuff.com/chapter16/
    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.ehlo()
    server.starttls()
    server.login('tucorreo', 'tucontraseña')
    server.sendmail(from_addr='tucorreo', to_addrs=to, msg=content)
    server.close()

def screenShot():
    img = pyautogui.screenshot()
    img.save("C://Users//mivegaal//Desktop//asistente-voz//ss.png")

def cpu():
    usage = str(psutil.cpu_percent())
    speak("La CPU está en un porcentaje de uso de " + usage)
    battery = psutil.sensors_battery()
    speak("La bateria tiene un " + str(battery.percent) + " porciento de carga")

def jokes():
    speak(pyjokes.get_joke(language = 'es'))

if __name__ == "__main__":
    wishme()
    while True:
        query = takeCommand().lower()

        if 'hora' in query:
            time()
        elif 'fecha' in query:
            date()
        elif 'wikipedia' in query:
            speak("Buscando tu consulta...")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences=2)
            print(result)
            speak(result)
        elif 'enviar correo' in query:
            try:
                speak("¿Qué quieres enviar por correo?")
                content = takeCommand()
                to = 'correoaquienenviaras'
                sendEmail(to, content)
                speak("Tu correo ha sido enviado señor!")
            except Exception as e:
                print(e)
                speak("No pude enviar tu correo señor!")
        elif 'buscar en firefox' in query:
            speak("Qué desea buscar en firefox")
            firefoxpath = 'C:/Program Files/Mozilla Firefox/firefox.exe %s'
            search = takeCommand().lower()
            wb.get(firefoxpath).open_new_tab(search + '.com')
        elif 'cerrar sesión' in query:
            os.system("shutdown -l")
        elif 'apagar' in query:
            os.system("shutdown /s /t l")
        elif 'reiniciar' in query:
            os.system("shutdown /r /t l")
        elif 'escuchar música' in query:
            songs_dir = 'C:/Users/mivegaal/Downloads/musica'
            songs = os.listdir(songs_dir)
            os.startfile(os.path.join(songs_dir, songs[0]))
        elif 'recuerda esto' in query:
            speak("¿Qué desea recordar señor?")
            data = takeCommand()
            speak("Lo que debo guardar es: " + data)
            remember = open('data.txt', 'w')
            remember.write(data)
            remember.close()
        elif 'algo que deba recordar' in query:
            remember = open('data.txt', 'r')
            speak("Si señor, recuerda que " + remember.read())
        elif 'captura de pantalla' in query:
            screenShot()
            speak("Captura realizada, señor!")
        elif 'recursos del sistema' in query:
            cpu()
        elif 'broma' in query:
            jokes()
        elif 'salir' in query:
            quit()
