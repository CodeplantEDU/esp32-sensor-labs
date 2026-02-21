# 🌞 ESP32 조도센서 강의자료

## 📘 1. 조도센서 개요

조도센서는 **주변 밝기(빛의 세기)를 전기 신호로 변환하여 낮/밤 판단 또는
밝기 수치(ADC, Lux)로 활용하는 센서**입니다.

### ✔ 실생활 활용 예

-   가로등 자동 점등 시스템
-   스마트폰 자동 밝기 조절
-   무드등 밝기 제어
-   실내 자동 조명 시스템

## 🔬 2. 조도센서 동작 원리 (CdS 기반)

조도센서는 **황화카드뮴셀(CdS, Cadmium Sulfide)** 을 사용합니다.

-   빛을 비추면 → 전류 증가 → 저항 감소
-   빛을 가리면 → 전류 감소 → 저항 증가

> 밝을수록 저항 ↓\
> 어두울수록 저항 ↑

기본 전기식:

R = V / I

## 🔌 3. 전압 분배 회로 구조

조도센서는 전압 분배(Voltage Divider) 형태로 사용됩니다.

### 📐 기본 구조

    Vcc
     │
    LDR
     │── Vout (ADC 입력)
     │
     R (고정저항)
     │
    GND

출력 전압 공식:

Vout = Vcc × R / (LDR + R)

### 🔎 분압 위치에 따른 값 변화

  LDR 위치   밝을 때    어두울 때
  ---------- ---------- -----------
  위쪽       ADC 증가   ADC 감소
  아래쪽     ADC 감소   ADC 증가

모듈 구조에 따라 ADC 값이 반대로 나올 수 있으므로 코드에서 반전 처리가
필요할 수 있습니다.

## 🎛 4. AO와 DO 차이

  핀    설명
  ----- ---------------------------------------
  VCC   5V (일부 3.3V 가능, 모듈 사양 확인)
  GND   공통 접지
  AO    아날로그 출력 (밝기 → 전압 변화)
  DO    디지털 출력 (임계값 기준 ON/OFF 판단)

감도 조절 가변저항은 **디지털 출력 전환 기준 밝기(임계값)** 를
설정합니다.

## 📱 5. 프로젝트 개요 --- 스마트폰 자동 밝기 시스템

조도 감지 → ADC 변환 → 필터링 → 정규화 → 감마 보정 → PWM 출력 → LED 밝기
조절

## 🧠 6. 핵심 알고리즘 설명

### 1️⃣ EMA 필터

filtered = (1 - ALPHA) \* filtered + ALPHA \* 현재값

### 2️⃣ map01()

센서 값을 0\~1 범위로 정규화

### 3️⃣ clamp()

값이 0\~1 범위를 넘지 않도록 제한

### 4️⃣ 감마 보정

ratio = ratio \*\* GAMMA

## 💻 7. 최종 실습 코드

``` python
from machine import Pin, ADC, PWM
import time

PIN_AO = 34
PIN_DO = 14
PIN_LED = 25

adc = ADC(Pin(PIN_AO))
adc.atten(ADC.ATTN_11DB)

do = Pin(PIN_DO, Pin.IN)
led = PWM(Pin(PIN_LED), freq=5000)

ALPHA = 0.1
GAMMA = 2.4
INV_MIN = 3200
INV_MAX = 3800

def clamp(x, lo, hi):
    return lo if x < lo else hi if x > hi else x

def map01(x, x0, x1):
    return (x - x0) / (x1 - x0) if x1 != x0 else 0

filtered = 4095 - adc.read()

while True:
    raw = adc.read()
    inv = 4095 - raw
    digital = do.value()

    filtered = (1 - ALPHA) * filtered + ALPHA * inv

    ratio = map01(filtered, INV_MIN, INV_MAX)
    ratio = clamp(ratio, 0.0, 1.0)
    ratio = ratio ** GAMMA

    duty = 0 if digital == 1 else int(ratio * 65535)
    led.duty_u16(duty)

    print(f"밝기:{ratio*100:5.1f}% | ADC:{raw:4d} | LED:{duty:5d}")
    time.sleep(0.1)
```

## 🎯 학습 정리

-   센서 동작 원리
-   전압 분배 회로
-   ADC 변환
-   필터링 알고리즘
-   감마 보정
-   PWM 제어

임베디드 시스템 설계의 기본 구조를 이해하는 종합 실습입니다.
