#include <IRremote.h>
#include <Servo.h>

// Variáveis de controle
#define A 0xFF02FD   // anda para frente
#define B 0xFF9867   // anda para tras
#define C 0xFFE01F   // para a esquerda
#define D 0xFF906F   // para a direita
#define F 0xFFA857   // parar
#define KEY0 0xff6897  // música
#define KEY_STAR 0xFF30CF  // seguidor de linha
#define KEY_HASH 0xFF18E7  // autônomo

// Pinos
#define RECV_PIN  12  // recebe os sinais do controle
#define ECHO_PIN  7   // sensor ultrassônico (ECHO)
#define TRIG_PIN  8   // sensor ultrassônico (TRIG)
#define ENA 5         // motores velocidade
#define ENB 6
#define IN1 9         // motores direção
#define IN2 10
#define IN3 11
#define IN4 3
#define LED_Pin 13    // LED
#define LineTeacking_Pin_Left  A0  // seguidor de linha
#define LineTeacking_Pin_Middle A2
#define LineTeacking_Pin_Right  A3
#define carSpeed 220    // velocidade máxima
#define lowSpeed 150    // velocidade mínima

// Buzina
int speakerPin = 15;
int length = 15;
char notes[] = "ccggaagffeeddc "; 
int beats[] = { 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 4 }; // duração de cada nota
int tempo = 300;

// Funções para tocar música
void playTone(int tone, int duration) {
  tone(speakerPin, tone, duration);
  delay(duration);
  noTone(speakerPin);
}

void playNote(char note, int duration) {
  int tone = 0;
  switch(note) {
    case 'c': tone = 261; break;
    case 'd': tone = 294; break;
    case 'e': tone = 329; break;
    case 'f': tone = 349; break;
    case 'g': tone = 392; break;
    case 'a': tone = 440; break;
    case 'b': tone = 493; break;
    case ' ': tone = 0; break;  // pausa
  }
  if (tone > 0) {
    playTone(tone, duration);
  } else {
    delay(duration);  // pausa
  }
}

void sound() {
  for (int i = 0; i < length; i++) {
    playNote(notes[i], beats[i] * tempo);
  }
}

// Configuração do servo motor
Servo servo;

// Inicialização do receptor IR
IRrecv irrecv(RECV_PIN);
decode_results results;
unsigned long val;
unsigned long IR_PreMillis; // controla o intervalo entre os comandos
unsigned long LT_PreMillis;
int rightDistance = 0, leftDistance = 0, middleDistance = 0; // mede a distância

// Enumerações para modos de função e movimento
enum FUNCTIONMODE { 
  IDLE,
  LineTeacking,
  ObstaclesAvoidance,
  Bluetooth,
  IRremote
} func_mode = IDLE;

enum MOTIONMODE {
  STOP,
  FORWARD,
  BACK,
  LEFT,
  Music,
  RIGHT
} mov_mode = STOP;

void delays(unsigned long t) {
  unsigned long start = millis();
  while (millis() - start < t) {
    getIRData();  // Checar IR durante o delay
  }
}

int getDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  
  int duration = pulseIn(ECHO_PIN, HIGH);
  int distance = duration * 0.034 / 2;
  return distance;
}

// Funções de movimento do carro
void forward(bool debug = false) {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, carSpeed);
  analogWrite(ENB, carSpeed);
}

void back(bool debug = false) {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, carSpeed);
  analogWrite(ENB, carSpeed);
}

void left(bool debug = false) {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, lowSpeed);
  analogWrite(ENB, carSpeed);
}

void right(bool debug = false) {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, carSpeed);
  analogWrite(ENB, lowSpeed);
}

void stop(bool debug = false) {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}

void getIRData() {
  if (irrecv.decode(&results)) {
    val = results.value;
    irrecv.resume();
  }
}

// Configuração inicial do Arduino
void setup() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(LED_Pin, OUTPUT);
  servo.attach(4);  // Configurar pino do servo
  irrecv.enableIRIn();  // Inicializa IR
}

// Loop principal
void loop() {
  getIRData();
  // Verificar comandos e executar ações
}
