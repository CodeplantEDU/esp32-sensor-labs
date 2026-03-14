# 🌊 ESP32 수위 감지 및 RGB LED 경보 시스템 (MicroPython)

이 프로젝트는 **ESP32**와 **수위 감지 센서**, **RGB LED**를 활용하여 실시간으로 수위를 측정하고, 수량에 따라 단계별 LED 경보를 출력하는 임베디드 실습 프로젝트입니다.

## 🎯 실습 목표
* ESP32의 **ADC(Analog-to-Digital Converter)** 기능을 이해하고 수위 센서의 아날로그 값을 읽어옵니다.
* 수위 센서의 전도 원리(저항 변화)를 파악합니다.
* 조건문(`if-elif-else`)을 활용해 수위 단계별로 **초록(안전) → 파랑(주의) → 빨강(위험)** LED를 제어합니다.

---

## 🛠 준비물
| 부품명 | 상세 사양 | 수량 |
| :--- | :--- | :--- |
| **ESP32** | DevKit V1 | 1개 |
| **수위 센서** | 접촉식 보드형 (Analog Output) | 1개 |
| **RGB LED** | 공통 음극(Common Cathode) | 1개 |
| **브레드보드** | 400홀 이상 권장 | 1개 |
| **점퍼선** | M-F, M-M 타입 | 다수 |

---

## 🔌 회로 연결 (Wiring)
수위 센서는 아날로그 신호를 출력하므로 ESP32의 ADC 지원 핀인 **GPIO34**에 연결해야 합니다.

| 출발 (부품/핀) | 도착 (ESP32 핀) | 설명 |
| :--- | :--- | :--- |
| **수위 센서 VCC (+)** | 3.3V | 센서 전원 공급 |
| **수위 센서 GND (-)** | GND | 회로 공통 접지 |
| **수위 센서 SIG (S)** | **GPIO 34 (ADC)** | 수위 아날로그 신호 전달 |
| **RGB LED R** | **GPIO 25** | 위험(High) 상태 표시 |
| **RGB LED G** | **GPIO 26** | 안전(Low) 상태 표시 |
| **RGB LED B** | **GPIO 27** | 주의(Mid) 상태 표시 |
| **RGB LED GND** | GND | LED 공통 접지 |

---

## 📊 수위 단계별 동작 정의

| 수위 값 (0~4095) | 상태 판정 | LED 색상 | 설명 |
| :--- | :--- | :--- | :--- |
| **0 ~ 500** | **안전 (LOW)** | 🟢 초록색 | 물이 없거나 매우 낮은 상태 |
| **500 ~ 1800** | **주의 (MID)** | 🔵 파랑색 | 물이 중간 정도 차오른 상태 |
| **1800 이상** | **위험 (HIGH)** | 🔴 빨강색 | 물이 넘칠 위험이 있는 상태 |

> **Note:** 측정값은 물의 순도나 센서 상태에 따라 다를 수 있습니다. 정확한 제어를 위해 실습 전 임계값 테스트를 권장합니다.

---

## 💻 코드 (Python)

### 1. 아날로그 수위 값 읽기 (`lab1_water_raw_read.py`)
```python
from machine import Pin, ADC
import time

# ADC 설정 (GPIO34, 12비트 해상도)
water_adc = ADC(Pin(34))
water_adc.atten(ADC.ATTN_11DB) # 0~3.6V 범위 측정 설정

print("[실습1] 수위 값 읽기 시작")

while True:
    val = water_adc.read()
    print(f"현재 수위 값: {val}")
    time.sleep(0.1)
```

### 2. 수위별 3색 LED 경보 시스템 (`lab2_water_level_alert.py`)
```python
from machine import Pin, ADC
import time

# [핀 및 ADC 설정]
water_adc = ADC(Pin(34))
water_adc.atten(ADC.ATTN_11DB)

led_r = Pin(25, Pin.OUT)
led_g = Pin(26, Pin.OUT)
led_b = Pin(27, Pin.OUT)

def all_off():
    """모든 LED 핀을 끕니다."""
    led_r.value(0)
    led_g.value(0)
    led_b.value(0)

print("[실습2] 수위별 LED 경보 시스템 가동")

while True:
    val = water_adc.read()
    all_off() # 이전 상태 초기화
    
    if val < 500:
        led_g.value(1) # 초록색
        status = "SAFE"
    elif val < 1800:
        led_b.value(1) # 파랑색
        status = "WARNING"
    else:
        led_r.value(1) # 빨강색
        status = "DANGER"
        
    print(f"Value: {val:4d} | Status: {status}")
    time.sleep(0.5)
```

---

## ⚠️ 문제 해결 (Troubleshooting)
1. **값이 계속 0으로 나옵니다**: 센서의 VCC/GND 연결을 확인하고, SIG 핀이 ADC 사용이 가능한 GPIO34에 꽂혔는지 확인하세요.
2. **LED 색상이 섞여서 나옵니다**: `all_off()` 함수가 매 루프 시작 시 호출되어 이전 핀 출력을 초기화하는지 확인하세요.
3. **센서 부식 방지**: 실습 종료 후에는 센서 표면의 물기를 닦아 보관해야 전극의 부식을 막고 오래 사용할 수 있습니다.

---
*본 가이드는 CODEPLANT 교육 자료를 바탕으로 작성되었습니다.*
