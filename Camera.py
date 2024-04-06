import cv2 #biblioteca opencv

#classificador Haar Cascade para detecção de faces frontais
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#inicializa a captura de vídeo usando a câmera padrão (normalmente 0, mas pode variar)
cap = cv2.VideoCapture(0)

#define a resolução (1920x1080)
cap.set(3, 1920)  # Largura
cap.set(4, 1080)  # Altura

#loop para capturar continuamente quadros da camera
while True:
    #captura um quadro da câmera 
    ret, frame = cap.read()
    #frame armazena e ret indica se a cap foi bem sucedida
    if not ret:
        break

    #converte o quadro para escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #detecta faces no quadro
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    #desenha retângulos ao redor das faces detectadas
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    #exibi o quadro resultante
    cv2.imshow('Reconhecimento Facial', frame)

    #sair do loop quando a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#liberam os recursos e fecham a janela de visualização
cap.release()
cv2.destroyAllWindows()
