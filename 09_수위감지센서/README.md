🌊 ESP32 수위 감지 센서 & 3색 LED 연동 실습

본 프로젝트는 ESP32와 수위 감지 센서를 활용하여 물의 높이를 측정하고, 수위에 따라 RGB LED의 색상을 변경하여 상태를 시각화하는 메이킹 실습 가이드입니다.

📑 강의 자료 슬라이드 요약

[Slide 1] 실습 개요 및 목표

주제: 수위 센서의 원리 이해 및 데이터 시각화

목표: * 수위 센서의 아날로그 출력 원리를 이해한다.

ESP32의 ADC(Analog to Digital Converter) 기능을 익힌다.

수위에 따른 조건문 제어를 통해 RGB LED를 제어한다.

[Slide 2] 수위 감지 센서란?

물의 유무나 높이를 측정하는 센서입니다.

작동 방식: 센서 표면의 전극 노출 패턴에 물이 닿으면 저항값이 변하는 원리를 이용합니다.

특징: 물에 잠기는 면적이 넓을수록 출력되는 아날로그 값이 커집니다.

[Slide 3] 센서 핀 구조 (Pinout)

VCC: 전원 공급 (3.3V ~ 5V)

GND: 접지 (0V)

SIG/S: 아날로그 신호 출력 핀 (ESP32의 ADC 핀에 연결)

[Slide 4] RGB LED (3색 LED) 제어

하나의 LED 안에 Red, Green, Blue 소자가 들어있습니다.

각 핀에 신호를 주어 다양한 색 조합을 만듭니다.

이번 실습에서는 **낮음(Green) / 중간(Blue) / 높음(Red)**으로 상태를 표시합니다.

🛠 하드웨어 구성 (Pin Map)

부품

핀 이름

ESP32 연결 번호

수위 센서

SIG (S)

GPIO 34 (ADC)

RGB LED

R (Red)

GPIO 25

RGB LED

G (Green)

GPIO 26

RGB LED

B (Blue)

GPIO 27

공통

VCC / GND

3.3V / GND

💻 실습 코드 (Arduino IDE / C++)

/*
 * ESP32 Water Level Sensor with RGB LED
 * 수위에 따른 LED 색상 변화 실습
 */

// 핀 번호 설정
const int WATER_PIN = 34; // 수위 센서 (ADC)
const int LED_R = 25;     // 빨강
const int LED_G = 26;     // 초록
const int LED_B = 27;     // 파랑

void setup() {
  Serial.begin(115200);
  
  // LED 핀을 출력으로 설정
  pinMode(LED_R, OUTPUT);
  pinMode(LED_G, OUTPUT);
  pinMode(LED_B, OUTPUT);
  
  Serial.println("수위 감지 시스템을 시작합니다.");
}

void loop() {
  // 수위 값 읽기 (0 ~ 4095)
  int waterValue = analogRead(WATER_PIN);
  Serial.print("현재 수위 값: ");
  Serial.println(waterValue);

  // 모든 LED 끄기 (초기화)
  digitalWrite(LED_R, LOW);
  digitalWrite(LED_G, LOW);
  digitalWrite(LED_B, LOW);

  // 수위에 따른 조건 제어
  if (waterValue < 500) {
    // 수위 낮음: 초록색 (안전)
    digitalWrite(LED_G, HIGH);
    Serial.println("상태: 안전 (낮음)");
  } 
  else if (waterValue >= 500 && waterValue < 1500) {
    // 수위 중간: 파랑색 (주의)
    digitalWrite(LED_B, HIGH);
    Serial.println("상태: 주의 (중간)");
  } 
  else {
    // 수위 높음: 빨강색 (위험)
    digitalWrite(LED_R, HIGH);
    Serial.println("상태: 위험 (높음)");
  }

  delay(500); // 0.5초 대기
}


📖 실습 상세 설명

데이터 수집: analogRead() 함수를 사용하여 센서로부터 0에서 4095 사이의 값을 읽어옵니다.

임계값(Threshold) 설정: * 실습 환경(물 종류, 용기 크기)에 따라 값이 다를 수 있으므로 시리얼 모니터를 통해 본인의 환경에 맞는 숫자로 코드를 수정해야 합니다.

시각적 피드백: if-else 조건문을 사용하여 특정 수위 범위를 지정하고, 해당 범위에 맞는 LED 핀에 HIGH 신호를 보냅니다.

주의사항: 수위 센서의 회로 부품(상단 부분)은 물에 닿지 않게 주의하세요! 합선의 위험이 있습니다.

본 가이드는 교육용으로 제작되었습니다.
