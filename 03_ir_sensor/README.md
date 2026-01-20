# IR 반사형 센서(3핀: SIG/VCC/GND) - ESP32 실습 (SIG = GPIO26)

ESP32 + 3핀 IR 반사형 센서 모듈(**SIG / VCC / GND**)을 이용해 **바닥 반사량**을 읽고, 임계값(threshold)으로 **검정 라인(테이프) 감지**까지 진행합니다.

---

## 0) 한 줄 목표
- **SIG 값을 읽어서** 흰 바닥/검정 라인을 구분하고, 코드로 **라인 감지 로직**을 만든다.

---

## 1) 준비물
- ESP32(DevKit)
- IR 반사형 센서 모듈(3핀: **SIG / VCC / GND**)
- 점퍼선
- (권장) 흰 종이 + 검정 테이프(라인)
- (선택) LED 1개 + 220Ω 저항(감지 결과를 눈으로 보기)

---

## 2) 배선(핀맵)

### 2-1) 빠른 배선
- IR **VCC** → ESP32 **3V3(3.3V)**
- IR **GND** → ESP32 **GND**
- IR **SIG** → ESP32 **GPIO26**

> 권장 전원: **3V3**부터 먼저 사용하세요.
> - 만약 센서가 5V 전용이라면(제품 설명이 5V only), **SIG 출력이 3.3V를 넘지 않는지** 반드시 확인해야 합니다.

### 2-2) 회로 연결표 (IR 센서 ↔ ESP32)

| 연결 목적 | 출발(부품/핀) | 도착(부품/핀) | 설명(한 줄) |
|---|---|---|---|
| 센서 전원(+) | IR 센서 VCC | ESP32 3V3 | 센서 구동 전원 |
| 센서 전원(-) | IR 센서 GND | ESP32 GND | 기준점(공통 접지) |
| 센서 출력 | IR 센서 SIG | ESP32 GPIO26 | 반사량에 따라 값이 변함 |

---

## 3) 센서가 하는 일(아주 짧게)
- 센서 앞쪽에서 **적외선(IR)을 쏘고**, 바닥에서 **반사되어 돌아오는 양**을 측정합니다.
- 보통
  - **흰색**: 반사가 많음
  - **검정색**: 반사가 적음
- 그래서 SIG 값이 **흰/검에 따라 달라지고**, 그 차이를 이용해 “라인 감지”를 합니다.

> 주의: 모듈마다 SIG 값이 **흰색에서 커질 수도/작아질 수도** 있습니다.
> 그래서 먼저 **실습1(원시값 확인)** 으로 방향을 확인합니다.

---

## 4) 실습 파일 목록(권장)
- **실습 1:** `lab1_ir_raw_read.py` (원시값 확인)
- **실습 2:** `lab2_ir_threshold.py` (임계값으로 라인 판별)
- **실습 2-1:** `lab2_1_ir_calibration.py` (자동 캘리브레이션으로 임계값 잡기)
- **실습 3:** `lab3_ir_line_event.py` (라인 감지 이벤트 + LED 표시)

---

# 실습 1) 원시값 확인(흰/검에서 값이 어떻게 바뀌나?)

## 1) 코드 전체 흐름(큰 그림)
- GPIO26을 **ADC(아날로그)** 로 읽어서 0~4095 값을 출력
- 값이 흰/검에서 어떻게 변하는지 확인

## 2) 코드
```python
from machine import Pin, ADC
import time

SIG_PIN = 26

adc = ADC(Pin(SIG_PIN))
adc.width(ADC.WIDTH_12BIT)      # 0~4095
adc.atten(ADC.ATTN_11DB)        # 0~3.3V 범위

print("[실습1] IR 원시값(ADC) 확인")
print("흰 종이 / 검정 테이프 위에 센서를 번갈아 대보세요")

while True:
    v = adc.read()
    print("ADC:", v)
    time.sleep(0.2)
```

## 3) 주요 코드 분석(짧게)
- `ADC(Pin(26))` : GPIO26의 전압을 숫자로 읽음
- `read()` : 0~4095 값(전압에 비례)
- 흰/검에서 값이 달라지면 정상

## 4) 체크 포인트
- 값이 **거의 안 변하면**: 센서를 바닥에서 3~10mm 정도로 높이 조절
- 값이 **항상 0 또는 항상 4095**에 가깝다면: 배선(VCC/GND/SIG) 다시 확인

---

# 실습 2) 임계값(threshold)으로 라인 판별

## 1) 코드 전체 흐름(큰 그림)
- 실습1에서 본 원시값을 바탕으로 `TH`(임계값)을 정함
- `라인인지(True/False)` 를 출력

## 2) 코드
```python
from machine import Pin, ADC
import time

SIG_PIN = 26

adc = ADC(Pin(SIG_PIN))
adc.width(ADC.WIDTH_12BIT)
adc.atten(ADC.ATTN_11DB)

TH = 2000          # <- 실습1 값 보고 조절!
BLACK_IS_SMALL = True  # 검정일 때 값이 더 작으면 True, 더 크면 False

print("[실습2] 임계값으로 라인 판별")

while True:
    v = adc.read()

    if BLACK_IS_SMALL:
        on_line = (v < TH)
    else:
        on_line = (v > TH)

    print("ADC:", v, "| LINE:", on_line)
    time.sleep(0.2)
```

## 3) 주요 코드 분석(짧게)
- `TH` : 흰/검을 나누는 기준선
- `BLACK_IS_SMALL` : 모듈마다 값 방향이 달라서 옵션으로 둠

## 4) 체크 포인트
- `LINE`이 항상 True/False로 고정이면
  - `TH`를 더 올리거나/내리거나
  - `BLACK_IS_SMALL`을 반대로 바꿔보세요.

---

# 실습 2-1) 자동 캘리브레이션(임계값을 자동으로 잡기)

## 1) 코드 전체 흐름(큰 그림)
- 3초 동안 **흰색**에서 측정해서 평균
- 3초 동안 **검정색**에서 측정해서 평균
- 두 평균의 중간을 `TH`로 자동 설정

## 2) 코드
```python
from machine import Pin, ADC
import time

SIG_PIN = 26
SAMPLE_N = 30

adc = ADC(Pin(SIG_PIN))
adc.width(ADC.WIDTH_12BIT)
adc.atten(ADC.ATTN_11DB)

def avg_samples(n=30, dt=0.1):
    s = 0
    for _ in range(n):
        s += adc.read()
        time.sleep(dt)
    return s // n

print("[실습2-1] 자동 캘리브레이션")
print("1) 지금부터 3초 후 흰 종이 위에 올려두세요")
time.sleep(3)
white = avg_samples(SAMPLE_N)
print("WHITE_AVG =", white)

print("2) 지금부터 3초 후 검정 테이프 위에 올려두세요")
time.sleep(3)
black = avg_samples(SAMPLE_N)
print("BLACK_AVG =", black)

TH = (white + black) // 2
BLACK_IS_SMALL = (black < white)

print("\n[결과]")
print("TH =", TH)
print("BLACK_IS_SMALL =", BLACK_IS_SMALL)
print("이제 LINE 판별을 시작합니다. (Ctrl+C로 종료)")

while True:
    v = adc.read()
    on_line = (v < TH) if BLACK_IS_SMALL else (v > TH)
    print("ADC:", v, "| LINE:", on_line)
    time.sleep(0.2)
```

## 3) 주요 코드 분석(짧게)
- `white`, `black` 평균을 직접 뽑아서 **TH를 자동 계산**
- `BLACK_IS_SMALL`도 자동으로 결정(검정이 더 작은 값이면 True)

---

# 실습 3) 라인 감지 이벤트 + LED 표시(선택)

## 1) 코드 전체 흐름(큰 그림)
- 실습2/2-1의 `TH`와 `BLACK_IS_SMALL`을 사용
- 라인을 감지하면 LED를 켜고, 아니면 끔

> ESP32 보드마다 내장 LED 핀이 다를 수 있습니다.
> 내장 LED가 안 켜지면 `LED_PIN`을 바꾸거나, 이 실습은 `print()`만 사용해도 됩니다.

## 2) 코드
```python
from machine import Pin, ADC
import time

SIG_PIN = 26
LED_PIN = 2   # 보드에 따라 다를 수 있음

adc = ADC(Pin(SIG_PIN))
adc.width(ADC.WIDTH_12BIT)
adc.atten(ADC.ATTN_11DB)

led = Pin(LED_PIN, Pin.OUT)

TH = 2000
BLACK_IS_SMALL = True

print("[실습3] 라인 감지 이벤트")

prev = None
while True:
    v = adc.read()
    on_line = (v < TH) if BLACK_IS_SMALL else (v > TH)

    # 상태 변화 감지(라인에 들어갔을 때만 메시지)
    if prev is None:
        prev = on_line
    elif on_line != prev:
        print("STATE CHANGED -> LINE:", on_line)
        prev = on_line

    led.value(1 if on_line else 0)
    time.sleep(0.05)
```

---

## 5) 자주 막히는 포인트(트러블슈팅)
- **값이 전혀 변하지 않음**
  - VCC/GND/SIG 배선부터 확인
  - 센서 높이(바닥과 거리) 조절
- **값은 변하는데 라인 판별이 이상함**
  - 실습1에서 흰/검 값이 어떤 방향인지 확인
  - `BLACK_IS_SMALL` 옵션을 반대로 바꿔보기
  - `TH`를 흰/검 평균 사이로 조정
- **GPIO26을 써도 되나요?**
  - 네, 입력으로 사용 가능합니다.
  - 단, GPIO26은 ESP32에서 **ADC2** 계열이라 **Wi‑Fi를 켜면 ADC 읽기가 안 될 수 있음**(이 실습은 Wi‑Fi 사용 안 하므로 보통 문제 없음).

---

## 6) 다음 확장(선택)
- IR 센서 2개(좌/우)로 확장해서 라인트레이서처럼 사용
- 모터 드라이버(L9110S)와 연결해서
  - `LINE=True`이면 정지
  - `LINE=False`이면 전진
  같은 간단한 제어부터 시작
