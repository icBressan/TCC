import speech_recognition as sr
import openai
from gtts import gTTS
from playsound import playsound
import os

# Sua chave de API da OpenAI
openai.api_key = "SUA_CHAVE_AQUI"

# Inicializa o reconhecedor de fala
rec = sr.Recognizer()

# Função para reconhecimento de fala
def recognize_speech():
    with sr.Microphone() as mic:  # with sr.Microphone(device_index=1) as mic:
        rec.adjust_for_ambient_noise(mic)
        print("Fale alguma coisa")
        audio = rec.listen(mic)
        try:
            frase = rec.recognize_google(audio, language="pt-BR")
            return frase
        except sr.UnknownValueError:
            print("Não entendi o que você disse. Tente novamente.")
            return None
        except sr.RequestError as e:
            print(f"Erro no serviço de reconhecimento de fala: {e}")
            return None

# Função para converter texto em áudio e reproduzir
def text_to_speech(text):
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
        if user_input and "RobIA" in user_input:
            text_to_speech("Estou à disposição, no que posso ajudar?")
            break

# Loop interativo
while True:
    wait_for_activation()  # Aguarda o comando de ativação
    while True:
        user_input = recognize_speech()
        if user_input:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_input}],
                max_tokens=max_tokens
            )
            response = completion.choices[0].message.content
            print("Assistente:", response)

            # Converter a resposta em áudio e reproduzir
            text_to_speech(response)
