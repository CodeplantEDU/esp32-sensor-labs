# 초음파 센서(HC-SR04) - 실습 1, 실습 2, 실습 3 (ESP32 + MicroPython/Thonny)

ESP32 + HC-SR04로 **거리(cm)**를 측정하고, 거리값으로 **LED/알림** 같은 간단한 제어까지 빠르게 체험하는 실습 세트입니다.

---

## 0) 한 줄 목표
- **TRIG(GPIO26)** 로 초음파를 쏘고, **ECHO(GPIO25)** 펄스 길이를 읽어 **거리(cm)**로 바꾼다.

---

## 1) 준비물
- ESP32(DevKit)
- HC-SR04 초음파 센서
- 점퍼선, 미니 브레드보드
- (실습2 선택) LED 1개 + 220Ω 저항
- (선택) 부저(피에조)

> **중요(보호):** HC-SR04의 **ECHO는 보통 5V**로 나옵니다. ESP32는 3.3V 입력이므로  
> **ECHO → ESP32(GPIO25)** 는 **분압(저항 2개) 또는 레벨시프터**를 강력 권장합니다.

---

## 2) 핀맵(고정)
- **TRIG = GPIO26**
- **ECHO = GPIO25**

### 회로 연결표 (ESP32 ↔ HC-SR04)
| 연결 목적 | 출발(부품/핀) | 도착(부품/핀) | 설명(한 줄) |
|---|---|---|---|
| 센서 전원(+) | ESP32 5V(VIN) | HC-SR04 VCC | HC-SR04는 보통 5V 권장 |
| 센서 전원(-) | ESP32 GND | HC-SR04 GND | 공통 접지 |
| 초음파 발사(TRIG) | ESP32 GPIO26 | HC-SR04 TRIG | 10µs 펄스로 발사 |
| 초음파 수신(ECHO) | HC-SR04 ECHO | ESP32 GPIO25 | **분압/레벨시프터 권장** |

### ECHO 분압(저항 2개) 추천
- **HC-SR04 ECHO → (1kΩ) → ESP32 GPIO25**
- **ESP32 GPIO25 → (2kΩ) → GND**  
  → 5V가 약 3.3V로 내려갑니다(간단/저렴/수업용으로 충분).

---

## 3) 폴더/파일 구조(추천)
```
02_ultrasonic_hcsr04/
 ├─ README.md
 └─ code/
     ├─ lab1_distance_print.py
     ├─ lab2_distance_led_threshold.py
     └─ lab3_distance_filter_avg.py
```

---

# 1) 코드 파일 목록
- **실습 1:** `code/lab1_distance_print.py`  (거리 출력)
- **실습 2:** `code/lab2_distance_led_threshold.py` (거리 임계값 LED)
- **실습 3:** `code/lab3_distance_filter_avg.py` (평균 필터로 안정화)

---

# 실습 1) 거리 출력 (기본 측정)

## 1) 코드 전체 흐름(큰 그림)
1. TRIG에 짧은 펄스(10µs) → 초음파 발사
2. ECHO가 HIGH인 시간(µs) 측정
3. 시간 → 거리(cm)로 변환해서 `print()`

## 2) 주요 코드 분석(핵심만)
- TRIG: “발사 스위치” (출력)
- ECHO: “왕복 시간 타이머” (입력)
- 거리 공식: `cm = us / 58` (수업용으로 외우기 쉬운 근사식)

## 3) 코드 (lab1_distance_print.py)
```python
from machine import Pin, time_pulse_us
import time

TRIG = Pin(26, Pin.OUT)
ECHO = Pin(25, Pin.IN)

def read_cm(timeout_us=30000):
    # TRIG 10us 펄스
    TRIG.value(0)
    time.sleep_us(2)
    TRIG.value(1)
    time.sleep_us(10)
    TRIG.value(0)

    # ECHO가 HIGH인 시간(마이크로초) 측정
    us = time_pulse_us(ECHO, 1, timeout_us)  # 1: HIGH 펄스
    if us < 0:
        return None  # timeout 등

    # 거리(cm) 근사식 (HC-SR04에서 자주 사용)
    return us / 58.0

print("[실습1] 거리 출력(cm)")
while True:
    d = read_cm()
    if d is None:
        print("timeout")
    else:
        print("{:.1f} cm".format(d))
    time.sleep(0.2)
```

### 체크 포인트(자주 막힘)
- 값이 **0 / timeout**: TRIG/ECHO 핀 번호, 공통 GND, 분압 연결 확인
- 값이 **심하게 튐**: 센서 정면에 평평한 물체(벽/책), 10~80cm에서 먼저 테스트

---

# 실습 2) 거리 임계값 (가까우면 LED ON)

> LED는 “거리 조건을 눈으로 확인”하기 가장 좋은 장치라 수업에 잘 맞습니다.

## 1) 추가 배선(LED)
- ESP32 GPIO **(예: GPIO2)** → 220Ω 저항 → LED(+)  
- LED(-) → GND

※ LED 제어 핀은 수업에서 편한 핀으로 바꿔도 됩니다.

## 2) 코드 전체 흐름(큰 그림)
- 거리를 읽고
- `if d < 15:` 같은 조건으로 LED를 켜고/끄기

## 3) 코드 (lab2_distance_led_threshold.py)
```python
from machine import Pin, time_pulse_us
import time

TRIG = Pin(26, Pin.OUT)
ECHO = Pin(25, Pin.IN)

LED = Pin(2, Pin.OUT)     # 원하는 핀으로 변경 가능
THRESH = 15.0             # cm

def read_cm(timeout_us=30000):
    TRIG.value(0); time.sleep_us(2)
    TRIG.value(1); time.sleep_us(10)
    TRIG.value(0)
    us = time_pulse_us(ECHO, 1, timeout_us)
    if us < 0:
        return None
    return us / 58.0

print("[실습2] 임계값 LED ({}cm 이하면 ON)".format(THRESH))
while True:
    d = read_cm()
    if d is None:
        LED.value(0)
        print("timeout")
    else:
        near = (d < THRESH)
        LED.value(1 if near else 0)
        print("{:.1f} cm  |  LED {}".format(d, "ON" if near else "OFF"))
    time.sleep(0.1)
```

### 체크 포인트
- LED가 반대로 동작하면(ON/OFF): LED 극성/배선 확인
- 거리가 안정적이지 않으면: 실습3(필터) 적용

---

# 실습 3) 값 안정화 (최근 5개 평균)

## 1) 코드 전체 흐름(큰 그림)
- 최근 N번 측정값을 모아서 평균을 내면 “튀는 값”이 줄어듭니다.
- N이 너무 크면 반응이 느려집니다(수업용: 3~7 추천).

## 2) 코드 (lab3_distance_filter_avg.py)
```python
from machine import Pin, time_pulse_us
import time

TRIG = Pin(26, Pin.OUT)
ECHO = Pin(25, Pin.IN)

N = 5  # 평균에 쓸 샘플 수

def read_cm(timeout_us=30000):
    TRIG.value(0); time.sleep_us(2)
    TRIG.value(1); time.sleep_us(10)
    TRIG.value(0)
    us = time_pulse_us(ECHO, 1, timeout_us)
    if us < 0:
        return None
    return us / 58.0

buf = []

print("[실습3] 평균 필터(N={})".format(N))
while True:
    d = read_cm()
    if d is not None:
        buf.append(d)
        if len(buf) > N:
            buf.pop(0)

    if len(buf) == 0:
        print("waiting...")
    else:
        avg = sum(buf) / len(buf)
        print("raw: {}  |  avg: {:.1f} cm".format(
            "timeout" if d is None else "{:.1f} cm".format(d),
            avg
        ))
    time.sleep(0.1)
```

---

## 4) 트러블슈팅(요약)
- **timeout만 나옴**: TRIG=GPIO26, ECHO=GPIO25 맞는지 / GND 공통 / 센서 VCC 5V 확인
- **ESP32가 리셋/멈춤**: ECHO 5V 직결 가능성 → **분압/레벨시프터** 적용
- **값이 튐**: 벽/책처럼 “평평한 물체”로 먼저 테스트, 평균필터(N=5) 적용
- **너무 가까우면 오히려 이상함**: HC-SR04는 초근거리(수 cm)는 부정확할 수 있음

---

## 5) 다음 확장(과제)
- 거리 < 10cm면 **모터 정지**, 거리 > 30cm면 **모터 전진(PWM)** 같은 융합 실습
- 거리로 **부저 톤/간격** 바꾸기(가까울수록 빠르게 삐삐)
