# PIR 기반 자동 서보모터 제어 (ESP32 + External 6V Power + Thonny)

ESP32와 PIR 인체 감지 센서를 사용하여  
**사람이 감지되면 서보모터가 자동으로 동작**하는 실습 프로젝트이다.
 
이번에는 **외부 6V 5A 전원으로 서보모터를 안정적으로 구동**하는 형태로 구성한다.

또한 코드는 **Arduino IDE용 C/C++ 코드가 아니라, Thonny에서 바로 업로드할 수 있는 MicroPython 코드** 기준으로 작성한다.

---

## 📌 프로젝트 개요

- **입력(Input)**: PIR 인체 감지 센서
- **처리(Processing)**: ESP32
- **출력(Output)**: 서보모터 회전 제어
- **개발 환경**: Thonny + MicroPython
- **전원(Power)**: 외부 6V 5A 전원으로 서보 구동

> 서보모터는 순간적으로 큰 전류를 요구할 수 있으므로  
> ESP32의 3.3V 또는 5V 핀에서 직접 전원을 공급하지 않고,  
> **별도의 6V 외부 전원**으로 구동하는 방식이 안전하다.

---

## 🎯 실습 목표

- PIR 센서의 디지털 출력 신호를 읽는다.
- ESP32에서 사람 감지를 조건으로 판단한다.
- 감지 시 서보모터를 특정 각도로 회전시킨다.
- 일정 시간이 지나면 원래 위치로 복귀시킨다.
- 외부 전원 사용 시 필요한 **공통 접지(Common GND)** 개념을 이해한다.
- Thonny를 이용해 ESP32에 MicroPython 코드를 업로드한다.

---

## 🧰 사용 부품

- ESP32 개발 보드
- PIR 인체 감지 센서 (HC-SR501)
- 서보모터 1개
- 외부 전원 공급기 6V 5A
- 점퍼선
- 브레드보드 또는 테스트 배선 환경

> **주의:** 사용하는 서보모터가 **6V 입력을 허용하는 모델인지 데이터시트로 반드시 확인**해야 한다.  
> 일부 소형 서보는 4.8V~6V 범위만 허용하며, 모델에 따라 허용 전압이 다르다.

---

## 🔌 핀맵 구성

### 1️⃣ PIR 센서 ↔ ESP32

| PIR 센서 핀 | ESP32 연결 | 설명 |
|---|---|---|
| VCC | 5V (VIN) | PIR 전원 |
| GND | GND | 공통 접지 |
| OUT | GPIO 26 | 감지 신호 입력 |

---

### 2️⃣ 서보모터 ↔ ESP32 + 외부 6V 전원

| 서보모터 선 | 연결 대상 | 설명 |
|---|---|---|
| VCC (빨강) | 외부 6V 전원 + | 서보 구동 전원 |
| GND (갈색/검정) | 외부 6V 전원 - | 서보 전원 GND |
| Signal (주황/노랑) | ESP32 GPIO 27 | PWM 제어 신호 |

---

### 3️⃣ 공통 접지 연결

아래 GND들은 반드시 서로 연결해야 한다.

- ESP32 GND
- PIR GND
- 외부 6V 전원 GND
- 서보모터 GND

> 이 공통 접지가 연결되지 않으면  
> ESP32의 PWM 신호 기준 전압이 맞지 않아 서보가 오동작하거나 아예 동작하지 않을 수 있다.

---

## 🖼️ 배선 개념도

```text
[PIR Sensor]
 VCC  -----------------> ESP32 VIN(5V)
 GND  -----------------> ESP32 GND
 OUT  -----------------> ESP32 GPIO26

[Servo Motor]
 Signal ---------------> ESP32 GPIO27
 VCC    ---------------> External 6V (+)
 GND    ---------------> External 6V (-)

[Common Ground]
 ESP32 GND ------------+
 PIR GND  -------------+----> External 6V (-)
 Servo GND ------------+
```

---

## ⚠️ 전원 연결 주의사항

1. **서보 전원은 ESP32에서 직접 공급하지 않는다.**  
   서보는 기동 순간이나 부하가 걸릴 때 순간 전류가 커진다.

2. **ESP32는 USB로 구동하고, 서보는 외부 6V 5A 전원으로 구동한다.**

3. **GND는 반드시 공통으로 묶는다.**

4. 서보가 떨리거나 ESP32가 재부팅되면, 전원 부족이나 접지 문제를 먼저 의심해야 한다.

5. 외부 전원 극성을 반대로 연결하면 서보나 보드가 손상될 수 있으므로, 배선 전에 반드시 확인한다.

---

## 🧠 동작 원리

1. PIR 센서가 사람의 움직임을 감지한다.
2. ESP32가 PIR OUT 핀의 HIGH 신호를 읽는다.
3. 감지되면 서보모터를 지정 각도로 회전시킨다.
4. 마지막 감지 시점부터 일정 시간 동안 해당 위치를 유지한다.
5. 시간이 지나면 서보모터를 초기 위치로 되돌린다.

예시 동작:

- 대기 상태: 0°
- 감지 상태: 90° 회전
- 마지막 감지 후 3초 경과: 다시 0° 복귀

---

## 💻 Thonny용 ESP32 MicroPython 코드

아래 코드는 **Thonny에서 ESP32에 바로 저장해서 실행할 수 있는 MicroPython 코드**이다.

파일명 예시:
- `main.py`

```python
from machine import Pin, PWM
from time import sleep_ms, ticks_ms, ticks_diff

PIR_PIN = 26
SERVO_PIN = 27

pir = Pin(PIR_PIN, Pin.IN)
servo = PWM(Pin(SERVO_PIN), freq=50)

hold_time = 3000  # 마지막 감지 후 유지 시간(ms)
last_detect = 0
servo_opened = False


def angle_to_duty(angle):
    """
    ESP32 MicroPython PWM duty range: 0~1023 (10-bit)
    50Hz 기준 주기: 20ms

    일반적인 서보 기준 예시:
    0도   -> 0.5ms
    90도  -> 1.5ms
    180도 -> 2.5ms

    사용하는 서보에 따라 500~2500us 범위는 조정이 필요할 수 있다.
    """
    min_us = 500
    max_us = 2500
    pulse_us = min_us + (max_us - min_us) * angle / 180
    duty = int((pulse_us / 20000) * 1023)
    return duty


def set_servo_angle(angle):
    angle = max(0, min(180, angle))
    servo.duty(angle_to_duty(angle))


# 초기 위치
set_servo_angle(0)
sleep_ms(500)

print("System start")

while True:
    if pir.value() == 1:
        last_detect = ticks_ms()

        if not servo_opened:
            set_servo_angle(90)
            servo_opened = True
            print("Motion detected -> Servo 90 deg")

    if servo_opened and ticks_diff(ticks_ms(), last_detect) > hold_time:
        set_servo_angle(0)
        servo_opened = False
        print("No motion -> Servo back to 0 deg")

    sleep_ms(50)
```

---

## 🛠️ Thonny 설정 방법

### 1. MicroPython 펌웨어 준비
ESP32에 **MicroPython 펌웨어**가 올라가 있어야 한다.

이미 MicroPython이 설치되어 있다면 바로 다음 단계로 진행하면 된다.

---

### 2. Thonny 인터프리터 설정
Thonny에서 아래 순서로 설정한다.

- **도구(Tools)** → **옵션(Options)**
- **Interpreter** 탭 선택
- 인터프리터를 **MicroPython (ESP32)** 로 선택
- 연결된 포트 선택

---

### 3. 코드 저장
위 코드를 Thonny에 붙여넣고,

- **파일 → 저장**
- 저장 위치를 **MicroPython device** 로 선택
- 파일명을 **main.py** 로 저장

그러면 ESP32가 부팅될 때 자동 실행된다.

---

## ✅ 예상 동작 결과

- 평상시: 서보모터가 0° 위치에서 대기
- 사람 감지 시: 서보모터가 90°로 회전
- 움직임이 계속 감지되면: 90° 상태 유지
- 마지막 감지 후 3초 경과 시: 0°로 복귀

---

## 🔍 실습 포인트

### 1. 왜 외부 전원이 필요한가
서보모터는 위치를 이동할 때 LED보다 훨씬 큰 전류 변동이 발생한다.  
그래서 ESP32 보드 전원만으로 구동하면 전압 강하나 재부팅 문제가 생기기 쉽다.

### 2. 왜 공통 접지가 필요한가
ESP32가 내보내는 PWM 신호는 GND를 기준으로 한다.  
외부 전원 GND와 ESP32 GND가 분리되어 있으면 신호 기준이 맞지 않는다.

### 3. PIR 센서의 특성
PIR 센서는 정적인 사람보다 **움직임 변화**에 더 민감하다.  
따라서 사람이 완전히 멈춰 있으면 감지가 약해질 수 있다.

### 4. 서보 각도 보정 필요
서보마다 실제 회전 범위와 중립점이 조금씩 다르다.  
필요하면 `min_us`, `max_us`, 목표 각도 값을 조정해야 한다.

---

## 🧪 응용 아이디어

- 감지 시 90°가 아니라 0° → 90° → 0° 왕복 동작
- PIR 감지 횟수를 카운트해서 시리얼 출력
- OLED 또는 LCD에 감지 상태 표시
- 감지 시간에 따라 서보 각도를 다르게 제어
- 여러 개의 PIR 센서를 사용해 방향별 동작 구현

---

## 🐞 트러블슈팅

### 1. 서보가 전혀 안 움직이는 경우
- 외부 6V 전원이 실제로 연결되어 있는지 확인
- 공통 GND 연결 여부 확인
- 서보 Signal 핀이 GPIO 27에 맞게 연결되었는지 확인
- 사용 중인 서보가 6V 허용 모델인지 확인

### 2. 서보가 떨리기만 하는 경우
- 전원 부족 가능성
- 배선 접촉 불량 가능성
- PWM duty 범위가 서보와 맞지 않을 가능성
- `min_us`, `max_us` 값을 조정해야 할 수 있음

### 3. PIR 감지가 너무 늦거나 불안정한 경우
- HC-SR501의 감도/지연 가변저항 설정 확인
- 전원 연결 안정성 확인
- 초기 부팅 직후 PIR 안정화 시간이 필요할 수 있음

### 4. ESP32가 재부팅되는 경우
- 서보 전원을 ESP32에서 직접 뽑아 쓰고 있는지 확인
- 공통 접지는 하되, 서보 전원 자체는 외부 전원에서 공급해야 함

---

## 📁 파일 구성 예시

```text
project-folder/
 ├─ main.py
 └─ README.md
```

---

## 📚 정리

이 실습은 단순히 PIR 센서를 읽는 것을 넘어서,

- **센서 입력 처리**
- **PWM 기반 액추에이터 제어**
- **외부 전원 분리 구동**
- **공통 접지 개념**
- **Thonny + MicroPython 기반 ESP32 개발 흐름**

을 한 번에 익힐 수 있는 기본 실습이다.

하드웨어 제어 프로젝트에서 매우 자주 등장하는 구조이므로, 이후 자동문, 쓰레기통 뚜껑, 로봇 암 초기 동작, 감지형 장치 제어 등으로 확장하기 좋다.
