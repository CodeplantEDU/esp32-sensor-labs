# IR 센서(근접/반사형) - SIG/VCC/GND (ESP32 GPIO26)

> ✅현재 사용 중인 IR 센서는 “흰/검 라인 구분”보다는 **물체가 가까운지(반사광이 충분한지)**를 더 잘 보여주는 **근접/반사형 IR 센서처럼 동작**합니다.
---
## 0) 한 줄 목표
IR 센서의 출력(SIG)을 **ESP32 GPIO26**에서 읽어서,
- (1) 센서 값이 어떻게 변하는지 확인하고
- (2) 임계값으로 **감지/미감지(ON/OFF)** 를 만들고
- (3) 오작동을 줄이는 **필터링(히스테리시스/평균)** 을 적용한다.

---

## 1) 준비물
- ESP32(DevKit)
- IR 센서 모듈 (핀 3개: **SIG / VCC / GND**)
- 점퍼선
- 브레드보드

(선택)
- Arduino Nano (아날로그 값 비교 테스트용)

---

## 2) 핀맵 / 배선

### (A) ESP32 배선 (권장)
| IR 센서 핀 | ESP32 | 설명 |
|---|---|---|
| **VCC** | **3V3** | 전원 (+) |
| **GND** | **GND** | 접지 (-) |
| **SIG** | **GPIO26** | 센서 출력(아날로그처럼 변할 수 있음) |

> **중요(공통 접지):** VCC/GND를 정확히 연결해야 값이 안정적으로 나옵니다.

### (B) Arduino Nano로 테스트할 때(참고)
| IR 센서 핀 | Arduino Nano | 설명 |
|---|---|---|
| **VCC** | **5V** | 전원 (+) |
| **GND** | **GND** | 접지 (-) |
| **SIG** | **A0** | `analogRead()`로 값 확인 |

---

## 3) 이 센서가 “라인(흰/검)”이 아니라 “근접”처럼 보이는 이유

### ✅ 관측한 패턴
- 물체가 가까우면: **값이 크게 올라가고 (예: ESP32에서 3000~3600 근처)**
- 멀어지면: **0 근처로 떨어짐**
- 검은선을 밟아도: 상황에 따라 **높은 값이 유지될 수 있음**

### ✅ 해석
이건 보통 아래 중 하나(또는 복합)입니다.
1. 센서가 바닥의 “흰/검 차이”보다 **거리(반사량 크기)**에 더 민감
2. 센서가 보는 방향/각도가 바닥이 아니라 **앞/옆 물체 반사**에 더 민감
3. 출력(SIG)이 연속값처럼 보이더라도 내부 회로 특성상 **0 또는 큰 값 위주로 뭉칠 수 있음**

---

## 4) 코드 파일 목록 (추천)
- **실습 1:** `lab1_ir_read_value_esp32.py` (ESP32에서 값 읽기)
- **실습 2:** `lab2_ir_threshold_onoff_esp32.py` (임계값으로 ON/OFF)
- **실습 3:** `lab3_ir_filter_hysteresis_esp32.py` (필터링/히스테리시스)

---

# 실습 1) IR 값 읽기 (ESP32)

## 1) 코드 전체 흐름(큰 그림)
- ADC(아날로그 입력) 준비
- `read_u16()` 또는 `read()`로 값 읽기
- 시리얼(Thonny)에서 값 변화 관찰

## 2) 주요 코드
> 파일: `lab1_ir_read_value_esp32.py`

```python
# [실습1] IR 센서 값 읽기 (ESP32 / MicroPython)
# 배선: SIG->GPIO26, VCC->3V3, GND->GND

from machine import Pin, ADC
import time

IR_PIN = 26
adc = ADC(Pin(IR_PIN))

# ESP32는 보통 ADC 범위 설정을 해주면 더 안정적입니다.
# (MicroPython 버전에 따라 지원 여부가 다를 수 있음)
try:
    adc.atten(ADC.ATTN_11DB)   # 측정 범위 넓힘(대략 0~3.3V)
    adc.width(ADC.WIDTH_12BIT) # 0~4095
except:
    pass

print("[실습1] IR 값 읽기 시작")

while True:
    try:
        # 12bit일 때: 0~4095
        val = adc.read()
    except:
        # read_u16() 지원이면: 0~65535
        val = adc.read_u16()

    print("IR =", val)
    time.sleep(0.1)
```

### 체크 포인트
- 값이 계속 **0**이면: VCC/GND 배선, SIG 배선, 핀 번호(GPIO26)부터 확인
- 값이 계속 **최대치에 가깝게 고정**이면: 센서가 너무 가까운 물체를 보고 있거나, SIG가 3.3V에 가까운 HIGH로 붙어있을 수 있음

---

# 실습 2) 임계값으로 감지/미감지 만들기 (ESP32)

## 1) 코드 전체 흐름(큰 그림)
- 실습1에서 값의 범위를 관찰
- 임계값(threshold)을 정함
- threshold 이상이면 “감지됨”, 미만이면 “미감지” 출력

## 2) 주요 코드
> 파일: `lab2_ir_threshold_onoff_esp32.py`

```python
# [실습2] IR 센서 임계값 감지 (ESP32 / MicroPython)
# 배선: SIG->GPIO26

from machine import Pin, ADC
import time

IR_PIN = 26
THRESHOLD = 2000  # <-- 실습1에서 본 값에 맞춰 조절

adc = ADC(Pin(IR_PIN))
try:
    adc.atten(ADC.ATTN_11DB)
    adc.width(ADC.WIDTH_12BIT)
except:
    pass

print("[실습2] threshold =", THRESHOLD)

while True:
    val = adc.read()

    if val >= THRESHOLD:
        print("DETECTED  | IR=", val)
    else:
        print("NO OBJECT | IR=", val)

    time.sleep(0.1)
```

### 체크 포인트
- `THRESHOLD`는 **정답이 하나가 아니라** 환경(조명/거리/각도/바닥)에 따라 바뀝니다.
- 수업에서는 보통:
  - 손을 가까이/멀리 하면서 값을 보고
  - 그 중간값을 임계값으로 잡게 하면 이해가 빠릅니다.

---

# 실습 3) 오작동 줄이기 (필터링 + 히스테리시스)

> 센서 값이 경계(threshold 근처)에서 흔들리면 출력이 **ON/OFF가 빠르게 깜빡**입니다.
> 이걸 줄이려고 **(1) 평균 필터** + **(2) 히스테리시스(ON/OFF 임계값을 다르게)** 를 사용합니다.

## 1) 코드 전체 흐름(큰 그림)
- 최근 N개 값을 평균내서 흔들림 줄이기
- ON 임계값 / OFF 임계값을 다르게 잡아서 깜빡임 줄이기

## 2) 주요 코드
> 파일: `lab3_ir_filter_hysteresis_esp32.py`

```python
# [실습3] 평균 필터 + 히스테리시스 (ESP32 / MicroPython)

from machine import Pin, ADC
import time

IR_PIN = 26

# 히스테리시스: ON은 높게, OFF는 낮게
TH_ON  = 2200
TH_OFF = 1800

N = 10  # 평균낼 샘플 수(클수록 부드러움, 반응은 느려짐)

adc = ADC(Pin(IR_PIN))
try:
    adc.atten(ADC.ATTN_11DB)
    adc.width(ADC.WIDTH_12BIT)
except:
    pass

buf = [0] * N
idx = 0
state = False  # False=미감지, True=감지

print("[실습3] TH_ON=", TH_ON, "TH_OFF=", TH_OFF, "N=", N)

while True:
    v = adc.read()

    buf[idx] = v
    idx = (idx + 1) % N
    avg = sum(buf) // N

    # 상태 전이
    if (not state) and (avg >= TH_ON):
        state = True
        print("--> DETECTED (avg=", avg, ")")

    elif state and (avg <= TH_OFF):
        state = False
        print("--> NO OBJECT (avg=", avg, ")")

    # 상태 출력
    print("state=", "ON" if state else "OFF", " raw=", v, " avg=", avg)
    time.sleep(0.05)
```

---

## 5) Arduino Nano 테스트 코드 (A0 읽기)
> 센서가 아날로그처럼 변하는지 확인할 때 유용합니다.

```cpp
// arduino_ir_read_a0.ino
// IR 센서 아날로그 값 측정 (Arduino Nano)
// 배선: SIG->A0, VCC->5V, GND->GND

const int IR_PIN = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int raw = analogRead(IR_PIN);          // 0~1023
  float volt = raw * (5.0 / 1023.0);     // Nano 5V 기준

  Serial.print("RAW=");
  Serial.print(raw);
  Serial.print("  V=");
  Serial.println(volt, 3);

  delay(100);
}
```

---

## 6) 자주 막히는 곳(트러블슈팅)

### (1) 검은선인데도 값이 높게 나와요
- 센서 높이를 조금 올리거나(바닥에서 멀리)
- 센서 각도를 바닥에 수직으로 맞추고
- 주변(옆/앞)에 반사되는 물체(손/벽/테이블 가장자리)가 없는지 확인하세요.

### (2) 값이 0 또는 최대치로만 나와요
- SIG가 **디지털 판정 출력**에 가까운 경우일 수 있습니다.
- 그럴 땐 실습2/3처럼 **threshold 기반 ON/OFF**로 쓰는 게 정석입니다.

### (3) ESP32에서 값 범위가 0~3600 정도로 보여요
- ESP32의 ADC는 12-bit일 때 보통 0~4095 범위입니다.
- 3600대는 “상당히 높은 입력(강한 반사/가까움)”이라는 뜻으로 이해하면 됩니다.

---

## 7) 다음 확장 아이디어(수업용)
- 감지되면 LED 켜기
- 감지되면 모터 정지(L9110S 실습과 연결)
- 두 개 센서를 좌/우에 붙여서 간단한 장애물 회피/라인트레이서 형태로 확장

---

## 라이선스(선택)
수업 자료로 자유롭게 사용하려면 아래처럼 넣어도 됩니다.
- MIT License 또는 CC BY

