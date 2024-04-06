import speech_recognition as sr
import openai
from gtts import gTTS
from playsound import playsound
import os

# Sua chave de API da OpenAI
openai.api_key = ""

# Inicializa o reconhecedor de fala
rec = sr.Recognizer()

# Função para reconhecimento de fala
def recognize_speech():
    with sr.Microphone(device_index=1) as mic:
        rec.adjust_for_ambient_noise(mic)
        print("Fale alguma coisa")
        audio = rec.listen(mic)
        frase = rec.recognize_google(audio, language="pt-BR")
        return frase

# Função para converter texto em áudio e reproduzir
def text_to_speech(text, speed=2.0):
    tts = gTTS(text, lang="pt", slow=False)  # Ajuste a velocidade com o argumento 'slow'
    audio_file = "output.mp3"
    tts.save(audio_file)
    playsound(audio_file)
    os.remove(audio_file)  # Exclui o arquivo de áudio após a reprodução

# Limite de tokens para respostas
max_tokens = 60  # Defina o número desejado de tokens aqui

# Comando de ativação
def wait_for_activation():
    while True:
        user_input = recognize_speech()
        if "Jarvis" in user_input:
            text_to_speech("Estou à disposição, no que posso ajudar?")
            break

# Loop interativo
while True:
    wait_for_activation()  # Aguarda o comando de ativação
    while True:
        user_input = recognize_speech()
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}],
            max_tokens=max_tokens
        )
        response = completion.choices[0].message.content
        print("Assistente:", response)

        # Converter a resposta em áudio e reproduzir com uma velocidade mais rápida (por exemplo, 1.5)
        text_to_speech(response, speed=2.0)
