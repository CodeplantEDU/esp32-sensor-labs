# Relay 기반 Servo Power ON/OFF 제어 실습 (ESP32 + Relay + External 6V 5A Servo Power)

ESP32와 릴레이 모듈, 서보모터를 이용하여  
**외부 6V 5A 전원으로 서보모터를 안전하게 켜고, ESP32의 PWM 신호로 각도를 제어하는 실습 프로젝트**이다.

이 실습은 PIR 센서를 사용하지 않는다.  
핵심은 다음 두 가지이다.

- **릴레이 모듈**: 서보모터의 외부 전원(6V)을 ON/OFF
- **ESP32 PWM**: 서보모터의 각도 제어

> 릴레이는 **서보의 전원 라인만 스위칭**한다.  
> 서보모터의 **제어 신호(PWM)는 ESP32 GPIO에서 직접 출력**해야 한다.  
> 즉, 릴레이는 서보를 "움직이게 하는 장치"가 아니라 **전원을 연결/차단하는 장치**다.

---

## 📌 프로젝트 개요

- **제어 보드**: ESP32
- **전원 스위칭**: 1채널 릴레이 모듈
- **구동 부하**: 서보모터
- **서보 전원**: 외부 6V 5A 어댑터
- **개발 환경**: Thonny + MicroPython

---

## 🧰 사용 부품

- ESP32 개발 보드
- 1채널 릴레이 모듈
- 서보모터 1개
- 외부 전원 어댑터 6V 5A
- 점퍼선
- 브레드보드(선택)
- USB 케이블 (ESP32 업로드용)

---

## ⚠️ 실습 목적과 주의사항

이 실습의 목적은 **릴레이로 서보 전원을 제어하고**, 전원이 들어온 상태에서 **ESP32가 PWM으로 각도를 제어하는 구조**를 이해하는 것이다.

반드시 아래 사항을 지켜야 한다.

1. **서보 전원은 ESP32에서 직접 공급하지 않는다.**  
   서보모터는 기동 순간 전류가 커서 ESP32 보드 전원만으로 안정적으로 구동하기 어렵다.

2. **릴레이는 서보의 전원선만 끊는다.**  
   PWM 신호선을 릴레이로 스위칭하면 안 된다.

3. **서보 GND와 ESP32 GND는 공통 접지(common ground)로 묶는다.**  
   그래야 PWM 신호 기준 전압이 맞는다.

4. **릴레이 접점은 서보 전원 +6V 라인에 넣는다.**  
   일반적으로 + 전원 라인을 스위칭하는 방식이 가장 직관적이다.

5. **릴레이를 너무 빠르게 반복 ON/OFF 하지 않는다.**  
   서보는 모터성 부하라서 전류 변화가 크고, 릴레이는 기계식 접점이므로 빠른 채터링 용도로 쓰는 부품이 아니다.

---

## 🔌 시스템 구성

이 프로젝트는 아래처럼 동작한다.

1. ESP32가 릴레이를 ON 시킴
2. 외부 6V 전원이 서보모터에 공급됨
3. ESP32가 PWM 신호를 출력하여 서보 각도 제어
4. 동작이 끝나면 릴레이를 OFF 시켜 서보 전원 차단

---

## 🔌 핀맵 구성

### 1️⃣ 릴레이 모듈 ↔ ESP32

| 릴레이 핀 | ESP32 연결 | 설명 |
|---|---|---|
| VCC | 5V (VIN) | 릴레이 코일 전원 |
| GND | GND | 공통 접지 |
| IN | GPIO 27 | 릴레이 제어 신호 |

> 아래 예제는 **LOW 트리거 릴레이 모듈 기준**으로 작성했다.  
> 사용 중인 릴레이 모듈이 HIGH 트리거라면 코드의 ON/OFF 정의를 바꿔야 한다.

---

### 2️⃣ 서보모터 ↔ ESP32 / 외부전원

| 서보 선 | 연결 대상 | 설명 |
|---|---|---|
| Signal | GPIO 26 | ESP32 PWM 제어 신호 |
| V+ | 릴레이 NO | 릴레이 ON 시 6V 공급 |
| GND | 외부전원 GND | 서보 전원 GND |

---

### 3️⃣ 릴레이 접점 ↔ 외부 6V 전원

| 연결 위치 | 연결 대상 | 설명 |
|---|---|---|
| 외부 6V 전원 (+) | 릴레이 COM | 스위칭할 전원 입력 |
| 릴레이 NO | 서보 V+ | 릴레이 ON 시 서보에 6V 공급 |
| 외부 6V 전원 (–) | 서보 GND | 서보 전원 GND |
| 외부 6V 전원 (–) | ESP32 GND | 공통 접지 |

---

## 🖼️ 배선 개념 요약

- **ESP32 GPIO 27 → 릴레이 IN**
- **ESP32 GPIO 26 → 서보 Signal**
- **외부전원 +6V → 릴레이 COM**
- **릴레이 NO → 서보 V+**
- **외부전원 GND → 서보 GND**
- **외부전원 GND ↔ ESP32 GND 공통 연결**

> 핵심은 **서보의 전원은 외부 6V**, **서보의 각도 제어는 ESP32 PWM**, **릴레이는 전원만 연결/차단**이라는 점이다.

---

## 💡 동작 원리

서보모터는 내부적으로 PWM 제어 신호를 받아 목표 각도로 이동한다.  
하지만 서보에 충분한 전원이 공급되지 않으면 떨림, 오동작, 리셋, 잡음 문제가 발생할 수 있다.

이 실습에서는:

- ESP32가 릴레이를 켜서 서보 전원을 공급하고
- 그 다음 PWM을 출력해 각도를 바꾸며
- 동작이 끝나면 릴레이를 꺼서 전원을 차단한다.

즉, **전원 제어와 위치 제어를 분리**해서 이해하는 실습이다.

---

## 🧠 Thonny용 ESP32 MicroPython 예제 코드

아래 코드는 Thonny에서 ESP32에 그대로 저장해서 실행할 수 있는 예제다.  
파일명은 `main.py`로 저장하면 된다.

```python
from machine import Pin, PWM
from time import sleep_ms, sleep

# =========================
# 핀 설정
# =========================
RELAY_PIN = 27
SERVO_PIN = 26

# LOW 트리거 릴레이 기준
RELAY_ON = 0
RELAY_OFF = 1

# =========================
# 릴레이 설정
# =========================
relay = Pin(RELAY_PIN, Pin.OUT)
relay.value(RELAY_OFF)

# =========================
# 서보 PWM 설정
# 일반적인 서보는 50Hz 사용
# =========================
servo = PWM(Pin(SERVO_PIN), freq=50)

# ESP32 MicroPython의 duty_u16 기준 사용
# 보편적인 예시값이며, 서보 모델에 따라 조정 필요
SERVO_MIN_US = 500
SERVO_MAX_US = 2500
SERVO_PERIOD_US = 20000   # 50Hz -> 20ms


def us_to_duty_u16(us):
    return int(us * 65535 / SERVO_PERIOD_US)


def angle_to_us(angle):
    if angle < 0:
        angle = 0
    if angle > 180:
        angle = 180
    return SERVO_MIN_US + (SERVO_MAX_US - SERVO_MIN_US) * angle / 180


def set_servo_angle(angle):
    pulse_us = angle_to_us(angle)
    servo.duty_u16(us_to_duty_u16(pulse_us))


def servo_power_on():
    relay.value(RELAY_ON)


def servo_power_off():
    relay.value(RELAY_OFF)


# =========================
# 메인 동작
# =========================
while True:
    print("Relay ON -> Servo power supplied")
    servo_power_on()
    sleep_ms(300)   # 전원 안정화 대기

    print("Move to 0 degree")
    set_servo_angle(0)
    sleep(1.5)

    print("Move to 90 degree")
    set_servo_angle(90)
    sleep(1.5)

    print("Move to 180 degree")
    set_servo_angle(180)
    sleep(1.5)

    print("Move back to 90 degree")
    set_servo_angle(90)
    sleep(1.5)

    print("Relay OFF -> Servo power cut")
    servo_power_off()
    sleep(3)
```

---

## ▶️ 실행 방법 (Thonny 기준)

1. ESP32를 USB 케이블로 PC에 연결한다.
2. Thonny를 실행한다.
3. 인터프리터를 **MicroPython (ESP32)** 로 설정한다.
4. 위 코드를 새 파일에 붙여넣는다.
5. 파일명을 `main.py`로 하여 ESP32 보드에 저장한다.
6. 실행 후 Shell 창에서 로그를 확인한다.

---

## ✅ 예상 동작

정상적으로 연결되었다면 다음 순서로 반복 동작한다.

1. 릴레이 ON
2. 서보 전원 인가
3. 서보가 0° → 90° → 180° → 90°로 이동
4. 릴레이 OFF
5. 서보 전원 차단
6. 잠시 대기 후 다시 반복

---

## 🛠️ 트러블슈팅

### 1. 서보가 떨리기만 하고 안 움직임
가능한 원인:
- 외부 전원 용량 부족
- GND 공통 연결 누락
- PWM 범위가 서보와 맞지 않음

점검 항목:
- 외부 6V 5A 전원이 제대로 연결되었는지 확인
- 외부전원 GND와 ESP32 GND가 연결되었는지 확인
- `SERVO_MIN_US`, `SERVO_MAX_US` 값을 조정

---

### 2. 릴레이는 동작하는데 서보가 안 움직임
가능한 원인:
- 서보 Signal선 미연결
- GPIO 번호 오배선
- 릴레이 접점 COM/NO 배선 오류

점검 항목:
- 서보 Signal이 GPIO 26에 연결되었는지 확인
- 릴레이 COM에 6V+, NO에 서보 V+가 맞는지 확인

---

### 3. ESP32가 리셋되거나 불안정함
가능한 원인:
- 서보 전원을 ESP32 쪽에서 직접 끌어오고 있음
- 서보 기동 시 전류 스파이크 영향
- 배선이 불안정함

점검 항목:
- 서보 전원은 반드시 외부 6V 어댑터 사용
- ESP32와 서보 전원 라인을 분리하고 GND만 공통 연결
- 전원선과 GND 배선을 짧고 안정적으로 구성

---

### 4. 릴레이가 반대로 동작함
가능한 원인:
- 사용 중인 릴레이가 HIGH 트리거 모듈임

해결 방법:
아래 두 줄을 바꿔서 테스트한다.

```python
RELAY_ON = 1
RELAY_OFF = 0
```

---

## 🔧 확장 아이디어

이 실습 이후에는 아래 방향으로 확장할 수 있다.

- 버튼 입력으로 릴레이 및 서보 동작 시작
- 가변저항으로 서보 각도 변경
- 초음파 센서 감지 시 서보 동작
- 릴레이 대신 MOSFET 기반 전원 스위칭 회로로 개선
- 서보 2개 이상 동시 제어

---

## 📘 학습 포인트 정리

이 실습에서 익혀야 할 핵심은 다음과 같다.

- ESP32 GPIO로 릴레이 제어하기
- 외부 전원과 제어 보드 전원을 분리하는 이유
- 공통 접지(common ground)의 필요성
- 서보모터의 PWM 각도 제어 방법
- 릴레이는 전원 스위칭용이고, PWM 제어용이 아니라는 점

---

## 📎 라이선스 / 참고

교육 및 실습용으로 자유롭게 수정 가능.

서보모터 모델마다 실제 동작 pulse width 범위가 다를 수 있으므로,  
실제 사용 중인 서보의 데이터시트를 확인하여 `SERVO_MIN_US`, `SERVO_MAX_US`를 조정하는 것을 권장한다.
