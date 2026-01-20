# 온습도 센서(DHT11) - VCC / DATA / GND (DATA=GPIO26)

ESP32(MicroPython/Thonny)로 **DHT11 온습도 센서**를 읽어오는 실습 자료입니다.

---

## 0) 이 실습의 한 줄 목표
ESP32가 DHT11의 **온도/습도 값을 2초마다 읽어서 출력**하고, 조건에 따라 간단한 알림(문자)을 만들 수 있다.

---

## 1) 준비물
- ESP32 DevKit (MicroPython 설치)
- DHT11 센서 모듈(핀: **VCC, DATA, GND**)
- 점퍼선 3개
- 브레드보드(선택)

---

## 2) 배선
> **핀 이름은 센서 보드에 적힌 글자(VCC/DATA/GND)를 그대로 따르세요.**

- DHT11 **VCC** → ESP32 **3V3** *(권장)*
- DHT11 **GND** → ESP32 **GND**
- DHT11 **DATA** → ESP32 **GPIO26**

### 연결 체크 포인트
- **GND 공통**이 안 되면 값이 안 읽힙니다.
- DHT11은 케이블이 길거나 노이즈가 있으면 불안정해질 수 있어요. *(짧게, 단단히 연결)*
- 모듈에 따라 DATA에 **풀업 저항(4.7k~10k)**이 이미 들어있는 제품이 많습니다.
  - 만약 값이 계속 `OSError`로 실패하면: DATA-3V3 사이에 10k 저항을 추가해보세요.

---

## 3) 회로 연결표 (DHT11 ↔ ESP32)

| 연결 목적 | 출발(부품/핀) | 도착(부품/핀) | 설명(한 줄) |
|---|---|---|---|
| 전원 공급 | DHT11 VCC | ESP32 3V3 | 센서 동작 전원 |
| 접지(필수) | DHT11 GND | ESP32 GND | 기준점 공유 |
| 데이터 | DHT11 DATA | ESP32 GPIO26 | 온습도 데이터 신호 |

---

## 4) 코드 파일 목록(추천)
- **실습 1:** `lab1_dht11_read_print.py` (온/습도 읽어서 출력)
- **실습 2:** `lab2_dht11_status_message.py` (조건에 따라 상태 메시지)
- **실습 3:** `lab3_dht11_average_filter.py` (여러 번 읽어서 평균내기)

---

# 실습 1) DHT11 값 읽어서 출력

## 1) 코드 전체 흐름(큰 그림)
- DHT11 객체 만들기 (`dht.DHT11(Pin(GPIO26))`)
- 2초마다 측정(`measure()`) 후 온도/습도 출력

## 2) 코드
```python
from machine import Pin
import dht
import time

sensor = dht.DHT11(Pin(26))   # DATA=GPIO26

print("[실습1] DHT11 온습도 읽기")
while True:
    try:
        sensor.measure()  # 측정(필수)
        t = sensor.temperature()  # °C
        h = sensor.humidity()     # %
        print("Temp:", t, "C | Hum:", h, "%")
    except Exception as e:
        print("Read error:", e)

    time.sleep(2)
```

## 3) 체크 포인트(자주 막히는 곳)
- **`measure()`를 빼먹으면** 값이 안 바뀌거나 오류가 납니다.
- DHT11은 **읽기 간격을 너무 짧게** 하면 실패할 수 있어요. (권장: **2초 이상**)
- 값이 `None`처럼 보이거나 실패가 잦으면 배선/풀업저항/전원(3.3V)부터 확인하세요.

---

# 실습 2) 상태 메시지 만들기(조건문)

## 1) 코드 전체 흐름
- 측정 후 온/습도에 따라 `"덥다/쾌적"` 같은 문구 출력

## 2) 코드
```python
from machine import Pin
import dht
import time

sensor = dht.DHT11(Pin(26))

print("[실습2] DHT11 상태 메시지")
while True:
    try:
        sensor.measure()
        t = sensor.temperature()
        h = sensor.humidity()

        if t >= 28:
            temp_msg = "덥다"
        elif t <= 18:
            temp_msg = "춥다"
        else:
            temp_msg = "쾌적"

        if h >= 70:
            hum_msg = "습함"
        elif h <= 30:
            hum_msg = "건조"
        else:
            hum_msg = "적당"

        print(f"T={t}C({temp_msg}) | H={h}%({hum_msg})")

    except Exception as e:
        print("Read error:", e)

    time.sleep(2)
```

---

# 실습 3) 평균내서 더 안정적으로 출력(간단 필터)

## 1) 코드 전체 흐름
- 3번 읽어서 평균을 내고(실패하면 건너뛰기) 더 안정적인 값을 출력

## 2) 코드
```python
from machine import Pin
import dht
import time

sensor = dht.DHT11(Pin(26))

print("[실습3] DHT11 평균 필터")
while True:
    temps = []
    hums = []

    for _ in range(3):
        try:
            sensor.measure()
            temps.append(sensor.temperature())
            hums.append(sensor.humidity())
        except:
            pass
        time.sleep(2)

    if len(temps) == 0:
        print("All reads failed")
    else:
        t_avg = sum(temps) / len(temps)
        h_avg = sum(hums) / len(hums)
        print("Avg Temp:", round(t_avg, 1), "C | Avg Hum:", round(h_avg, 1), "%")

    time.sleep(2)
```

---

## 5) 확장 아이디어(선택)
- OLED(SSD1306)로 온습도 표시
- 습도 70% 이상이면 부저/LED 켜기
- 시리얼 출력 로그를 CSV로 저장해 그래프 그리기

