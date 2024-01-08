import speech_recognition as sr
from gtts import gTTS
import os
import cv2
import pyttsx3   
import numpy as np
from PIL import Image
from io import BytesIO

#
#GEMINI-1
import textwrap
import google.generativeai as genai  
from markdown import Markdown
###
#

class Programa:
    
    @staticmethod
    def tomar_foto():
        # Inicializar la cámara
        camara = cv2.VideoCapture(0)

        if not camara.isOpened():
            print("Error al abrir la cámara.")
            return None

        # Capturar un solo cuadro (foto)
        ret, frame = camara.read()
        retval, buffer = cv2.imencode('.jpg', frame)
        # Crear un objeto BytesIO para almacenar la imagen en memoria
        img_bytes = BytesIO(buffer.tobytes())

        # Abrir la imagen desde BytesIO usando PIL
        img_pil = Image.open(img_bytes)

        # Puedes mostrar la imagen si lo deseas
        img_pil.show()
        # Liberar la cámara
        camara.release()

        if ret:
            return img_pil
        else:
            print("Error al capturar la foto.")
            return None

    @staticmethod
    def comandos():
        print("Esperando comandos...")

    @staticmethod
    def escuchar_comando():
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Escuchando...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            comando = recognizer.recognize_google(audio, language='es-ES')
            print("Comando reconocido:", comando)
            return comando.lower()
        except sr.UnknownValueError:
            print("No se pudo entender el comando.")
            return None
        except sr.RequestError as e:
            print("Error en la solicitud a Google Speech Recognition; {0}".format(e))
            return None

    @staticmethod
    def texto_a_voz(texto):
        engine = pyttsx3.init()
        engine.say(texto)
        engine.runAndWait()

    @staticmethod
    def texto_a_voz_no_stop(texto):
        engine = pyttsx3.init()
        engine.say(texto)
        engine.startLoop(False)
        engine.iterate()
        engine.endLoop() 

def main():
    programa = Programa()
    
    #GEMINI-2
    GOOGLE_API_KEY=  '-Tu api key aqui-'
    genai.configure(api_key=GOOGLE_API_KEY)
    
    def to_markdown(text):
        return Markdown().convert(textwrap.indent(text, '> ', predicate=lambda _: True))
    #

    while True:
        programa.comandos()

        comando = programa.escuchar_comando()

        if comando == "escanear foto":
            programa.texto_a_voz_no_stop("Apunta con el celular, 3, 2, 1, click")
            
            # Tomar la foto (asumes que tienes la función tomar_foto implementada)
            foto = programa.tomar_foto()
            programa.texto_a_voz_no_stop("Procesando...")
            ##GEMINI-3
            #result = model.generateContent(inputText,imageParts) 
            model = genai.GenerativeModel('gemini-pro-vision')
            response = model.generate_content(["Describe lo que ves en la foto, si hay obstaculos, señales de transito o algo similar", foto], stream=True)
            response.resolve()
            print(response)
            formatted_text = to_markdown(response.text)
            print(formatted_text)
            programa.texto_a_voz_no_stop(response.text)
            # Llamada a Gemini.Vision (debes tener la función implementada)
            response = ("holi") 

if __name__ == "__main__":
    main()
