import streamlit as st
import requests
import soundfile as sf
import os

# Título de la aplicación
st.title("Transcripción de notas de voz en español")

# Ingresar clave de API
api_key = st.text_input("Ingrese su clave de API")

# Cargar archivo de audio
audio_file = st.file_uploader("Cargar archivo de audio", type=["wav"])

# Botón para transcribir y generar texto adicional
if st.button("Transcribir y generar texto"):
    if api_key and audio_file is not None:
        # Guardar archivo de audio en el sistema
        audio_path = "audio.wav"
        with open(audio_path, "wb") as f:
            f.write(audio_file.getvalue())

        # Llamar a la API de Whisper para transcribir el audio
        url = "https://api.openai.com/v1/engines/whisper/transcriptions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "audio/wav",
        }
        files = {"audio": open(audio_path, "rb")}
        response = requests.post(url, headers=headers, files=files)

        if response.status_code == 200:
            # Obtener la transcripción del audio
            transcription = response.json()["transcriptions"][0]["text"]

            # Mostrar la transcripción en la aplicación
            st.success("Transcripción:")
            st.write(transcription)

            # Generar texto adicional utilizando el modelo Da Vinci
            prompt = f"Generar más texto basado en la transcripción: {transcription}"
            url = "https://api.openai.com/v1/engines/davinci-codex/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            data = {
                "prompt": prompt,
                "max_tokens": 100,
            }
            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                # Obtener el texto generado por el modelo
                generated_text = response.json()["choices"][0]["text"]

                # Mostrar el texto generado en la aplicación
                st.success("Texto generado:")
                st.write(generated_text)
            else:
                st.error("Error al generar texto. Por favor, inténtelo de nuevo más tarde.")

        else:
            st.error("Error al transcribir el audio. Por favor, inténtelo de nuevo más tarde.")

        # Eliminar el archivo de audio del sistema
        os.remove(audio_path)
    else:
        st.warning("Por favor, ingrese su clave de API y cargue un archivo de audio.")
