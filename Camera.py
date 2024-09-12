import cv2  # Biblioteca OpenCV

# Carrega o classificador Haar Cascade para detecção de faces
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Inicializa a captura de vídeo usando a câmera padrão
cap = cv2.VideoCapture(0)

# Verifica se a câmera foi aberta corretamente
if not cap.isOpened():
    print("Erro: Não foi possível acessar a câmera.")
    exit()

# Define a resolução da captura (1920x1080)
frame_width = 1920
frame_height = 1080
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

# Parâmetros da detecção de faces
scale_factor = 1.3  # Fator de escala para a detecção
min_neighbors = 5   # Número mínimo de vizinhos para uma região ser considerada face
min_size = (30, 30) # Tamanho mínimo da face detectada

# Loop para capturar e processar os quadros em tempo real
while True:
    # Captura um quadro da câmera
    ret, frame = cap.read()

    # Verifica se a captura foi bem-sucedida
    if not ret:
        print("Erro: Não foi possível capturar o quadro.")
        break

    # Converte o quadro para escala de cinza (necessário para detecção de faces)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detecta faces no quadro
    faces = face_cascade.detectMultiScale(gray, scaleFactor=scale_factor, minNeighbors=min_neighbors, minSize=min_size)

    # Desenha retângulos ao redor das faces detectadas
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Exibe o quadro resultante com as faces detectadas
    cv2.imshow('Reconhecimento Facial', frame)

    # Verifica se a tecla 'q' foi pressionada para sair do loop
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Libera os recursos e fecha as janelas abertas
cap.release()
cv2.destroyAllWindows()
