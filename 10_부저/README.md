# 버저(Buzzer) 강의자료 (Markdown) — Active / Passive + ESP32 실습

> 대상: 고등/입문 실습  
> 보드 기준: ESP32(3.3V)  
> 목표: 부저의 종류(Active/Passive) 이해 + ON/OFF + PWM(주파수) 제어 실습

---

## 0. 한 줄 요약
- **Active 부저**: 내부에 발진(구동) 회로가 있어 **전원/신호만 주면 “삐—”** (주파수 고정)  
- **Passive 부저**: 발진 회로가 없어 **PWM(주파수)을 줘야 소리**, 주파수 바꾸면 **음높이 변경(멜로디 가능)**

---

## 1. 학습 목표
- Active/Passive 부저의 구조적 차이를 설명할 수 있다.
- ESP32로 Active 부저를 **디지털 ON/OFF** 제어할 수 있다.
- ESP32 PWM(LEDC)로 Passive 부저의 **주파수(Hz)** 를 바꿔 음높이를 만들 수 있다.
- 간단한 경고음(패턴) 또는 2음 멜로디를 구현할 수 있다.

---

## 2. 준비물
- ESP32 DevKit 1개
- Active 버저 1개 (모듈형 또는 단품)
- Passive 버저 1개 (가능하면 준비)
- 점퍼선, 브레드보드
- (옵션) 저항 100~220Ω, 트랜지스터(큰 버저/전류 클 때)

---

## 3. 버저가 쓰이는 곳(동기)
- 로봇/차량: 장애물 경고, 후진 경고, 상태음
- 전자제품: 버튼 입력 확인음, 오류 경고음
- 타이머/알람: 시간 종료 알림
- 센서 프로젝트: 임계값 초과 시 경보(온습도/가스/거리)

---

## 4. Active vs Passive 차이(핵심 개념)
### 4.1 구조 차이
- **Active**: 내부에 `Drive circuit(발진/구동 회로)` 포함  
  → 외부가 주파수를 만들 필요 없음
- **Passive**: 내부에 발진 회로 없음(피에조 디스크/코일 중심)  
  → 외부가 주파수(PWM)를 만들어 줘야 함

### 4.2 제어 차이(실습 기준)
- **Active**: HIGH/LOW로 켜고 끄기(패턴 만들기 쉬움)
- **Passive**: PWM 주파수 변경으로 음높이(피치) 조절(멜로디 가능)

---

## 5. 외형으로 구분하는 법(팁)
> 외형만으로 100% 확정은 어려울 수 있어, “표기 + 간단 테스트”가 가장 확실함.

- 라벨에 `Active / DC 3-5V / Beep` → Active 가능성↑  
- 라벨에 `Frequency / Tone / PWM` → Passive 가능성↑  
- **5초 테스트**: 전원(또는 SIG HIGH)만으로 바로 울리면 Active, PWM 줘야 울리면 Passive

---

## 6. 배선(핀맵)
### 6.1 Active 버저(모듈/3핀 기준)
- **VCC(+) → 3.3V**
- **GND(–) → GND**
- **SIG → GPIO 25** (예시)

### 6.2 Passive 버저(단품/2핀 기준)
- **(+) → GPIO 25(PWM 가능 핀)**  
- **(–) → GND**

> 공통 주의: **GND는 반드시 공통**, 극성(+/–) 표시가 있는 제품은 방향을 지키기.

---

## 7. 실습 1: Active 버저 ON/OFF (비프 패턴)
### 목표
- 0.2초 삐 → 0.2초 무음 반복
- 디지털 출력으로 “스위치처럼” 제어한다.

### Arduino IDE(ESP32) 예제 코드
```cpp
// Active Buzzer ON/OFF (ESP32, Arduino IDE)
const int BUZZER = 25;

void setup() {
  pinMode(BUZZER, OUTPUT);
}

void loop() {
  digitalWrite(BUZZER, HIGH); // 울림
  delay(200);
  digitalWrite(BUZZER, LOW);  // 무음
  delay(200);
}
