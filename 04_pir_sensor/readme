# PIR 인체감지 센서(VIN / OUT / GND) - 실습 1, 실습 2, 실습 2-1, 실습 3 (ESP32 + MicroPython/Thonny)

ESP32 + PIR(인체감지) 센서로 **움직임 감지(0/1)** 를 읽고, 감지 신호로 **LED/이벤트 로직**을 만드는 실습 세트입니다.

---

## 0) 한 줄 목표
- **OUT(GPIO26)** 의 HIGH/LOW를 읽어 **움직임 감지**를 확인한다.

---

## 1) 준비물
- ESP32(DevKit)
- PIR 센서 모듈 (VIN / OUT / GND 타입)
- 점퍼선, 미니 브레드보드
- (실습2 선택) LED 1개 + 220Ω 저항

> **중요(워밍업):** PIR 센서는 전원을 넣은 뒤 **20~60초 정도 안정화 시간**이 필요할 수 있습니다.  
> 처음에는 값이 튈 수 있으니, 워밍업 후 테스트하세요.

---

## 2) 핀맵(고정)
- **PIR OUT = GPIO26**

### 회로 연결표 (ESP32 ↔ PIR)
| 연결 목적 | 출발(부품/핀) | 도착(부품/핀) | 설명(한 줄) |
|---|---|---|---|
| 센서 전원(+) | ESP32 5V(VIN) 또는 3V3 | PIR VIN | 모듈에 따라 5V 권장(보드 표기 확인) |
| 센서 전원(-) | ESP32 GND | PIR GND | 공통 접지 |
| 감지 신호 | PIR OUT | ESP32 GPIO26 | 움직임 감지(보통 HIGH=감지) |

### 연결 체크 포인트
- **GND 공통**(ESP32 GND ↔ PIR GND) 반드시 연결
- PIR OUT은 보통 **HIGH(1)=감지, LOW(0)=대기** 입니다(모듈에 따라 다를 수 있어 실습1에서 확인)
- ESP32는 3.3V 입력이므로, OUT이 5V로 나오는 특수 모듈이면 주의(대부분 PIR OUT은 3.3V HIGH)

---

## 3) 폴더/파일 구조(추천)
```
03_pir_sensor/
 ├─ README.md
 └─ code/
     ├─ lab1_pir_print.py
     ├─ lab2_pir_led.py
     ├─ lab2_1_pir_cooldown.py
     └─ lab3_pir_counter.py
```

---

# 1) 코드 파일 목록
- **실습 1:** `code/lab1_pir_print.py`  (감지 상태 출력)
- **실습 2:** `code/lab2_pir_led.py` (감지 시 LED ON)
- **실습 2-1:** `code/lab2_1_pir_cooldown.py` (감지 후 재감지 잠금)
- **실습 3:** `code/lab3_pir_counter.py` (감지 이벤트 카운트)

---

# 실습 1) PIR 감지 상태 출력 (기본)

## 1) 코드 전체 흐름(큰 그림)
1. OUT(GPIO26)을 입력으로 설정
2. 값이 바뀔 때만 출력(스팸 출력 방지)
3. HIGH면 MOTION, LOW면 IDLE

## 2) 주요 코드 분석(핵심만)
- `Pin(26, Pin.IN, Pin.PULL_DOWN)` : 기본값을 0으로 안정화(모듈에 따라 없어도 됨)
- “변화가 있을 때만” 출력하면 보기 편함

## 3) 코드 (lab1_pir_print.py)
```python
from machine import Pin
import time

PIR = Pin(26, Pin.IN, Pin.PULL_DOWN)

print("[실습1] PIR 상태 출력")
prev = PIR.value()

while True:
    cur = PIR.value()
    if cur != prev:
        print("MOTION" if cur == 1 else "IDLE")
        prev = cur
    time.sleep(0.05)
```

---

# 실습 2) 감지 시 LED ON (눈으로 확인)

## 1) 추가 배선(LED)
- ESP32 GPIO **(예: GPIO2)** → 220Ω 저항 → LED(+)  
- LED(-) → GND

## 2) 코드 전체 흐름(큰 그림)
- PIR이 1이면 LED ON, 0이면 LED OFF
- 콘솔에도 상태를 같이 출력

## 3) 코드 (lab2_pir_led.py)
```python
from machine import Pin
import time

PIR = Pin(26, Pin.IN, Pin.PULL_DOWN)
LED = Pin(2, Pin.OUT)  # 원하는 핀으로 변경 가능

print("[실습2] PIR -> LED")
while True:
    motion = PIR.value()
    LED.value(1 if motion else 0)
    print("MOTION" if motion else "IDLE")
    time.sleep(0.2)
```

### 체크 포인트
- LED가 반대로 동작하면: LED 극성/배선 확인
- 출력이 계속 1이면: 센서가 “시간 지연 유지” 상태일 수 있음(모듈 특성)

---

# 실습 2-1) 감지 후 재감지 잠금(쿨다운)

> PIR은 한 번 감지되면 일정 시간 HIGH를 유지하거나, 연속 감지가 발생할 수 있습니다.  
> 수업에서는 “감지 후 2초간은 무시” 같은 쿨다운을 넣으면 결과가 깔끔합니다.

## 1) 코드 전체 흐름(큰 그림)
- 감지(상승 에지)를 한 번 잡으면 이벤트 1회로 처리
- 이후 `cooldown_s` 동안은 추가 감지를 무시

## 2) 코드 (lab2_1_pir_cooldown.py)
```python
from machine import Pin
import time

PIR = Pin(26, Pin.IN, Pin.PULL_DOWN)
cooldown_s = 2.0

print("[실습2-1] 쿨다운(재감지 잠금) =", cooldown_s, "s")

last_fire = 0
prev = 0

while True:
    cur = PIR.value()

    # 상승 에지(0->1)만 이벤트로 처리
    if prev == 0 and cur == 1:
        now = time.ticks_ms()
        if time.ticks_diff(now, last_fire) > int(cooldown_s * 1000):
            print("MOTION EVENT!")
            last_fire = now
        else:
            print("ignored (cooldown)")

    prev = cur
    time.sleep(0.05)
```

---

# 실습 3) 감지 이벤트 카운트(기록)

## 1) 코드 전체 흐름(큰 그림)
- “상승 에지”를 감지 이벤트로 카운트
- 이벤트 번호와 시간을 같이 출력

## 2) 코드 (lab3_pir_counter.py)
```python
from machine import Pin
import time

PIR = Pin(26, Pin.IN, Pin.PULL_DOWN)

count = 0
prev = 0
t0 = time.ticks_ms()

print("[실습3] PIR 이벤트 카운트")
while True:
    cur = PIR.value()

    if prev == 0 and cur == 1:  # 상승 에지
        count += 1
        dt = time.ticks_diff(time.ticks_ms(), t0) / 1000
        print("EVENT #{:02d}  at {:.1f}s".format(count, dt))

    prev = cur
    time.sleep(0.05)
```

---

## 4) 트러블슈팅(요약)
- **계속 IDLE(0)만 나옴**: VIN/GND 배선, GPIO26 연결, 센서 워밍업(20~60초) 확인
- **계속 MOTION(1)만 나옴**: 센서가 HIGH 유지 시간 설정이 길거나, 주변 움직임/열원 영향 가능
- **값이 너무 튐**: 워밍업 후 테스트, 센서 각도/거리 조정, 쿨다운(실습2-1) 적용
- **보드가 불안정**: 전원(USB/어댑터) 안정화, GND 공통 확실히

---

## 5) 다음 확장(과제)
- 감지되면 모터 정지/경고 출력(모터 실습과 연결)
- 감지 횟수로 “사람 출입 카운트(단순)” 만들기
