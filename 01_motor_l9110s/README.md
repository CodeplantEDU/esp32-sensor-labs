# 모터드라이버(L9110S) - 실습 1, 실습 2, 실습 2-1, 실습 3

ESP32 + L9110S + TT모터(1개)를 이용해 **방향(정/역) 제어**와 **PWM 속도 제어**를 빠르게 체험하는 실습 세트입니다.

---

## 실습 목표
ESP32가 L9110S에 신호를 줘서 모터를 **정방향 → 정지 → 역방향 → 정지**로 제어하고,  
PWM으로 **속도(세기)** 를 조절할 수 있다.

---

## 준비물
- ESP32(DevKit)
- L9110S 모터드라이버
- TT모터 1개
- AA 배터리팩(4개 = 6V 권장)
- 점퍼선
- 미니 브레드보드

---

## 배선(모터 A채널)
- ESP32 **GPIO2** → L9110S **A-IA**
- ESP32 **GPIO4** → L9110S **A-IB**
- TT모터 선 2개 → L9110S **OA1 / OA2**
- 배터리(+) → L9110S **VCC(VM,+)**
- 배터리(-) → L9110S **GND(-)**
- ESP32 **GND** → L9110S **GND** (**공통접지 필수**)

---

## 회로 연결표 (ESP32 + L9110S + TT모터)
> **핵심:** 배터리(-), L9110S GND, ESP32 GND는 **반드시 공통 접지**로 연결해야 합니다.

| 연결 목적 | 출발(부품/핀) | 도착(부품/핀) | 설명(한 줄) |
|---|---|---|---|
| 모터 전원 공급 | 배터리팩 + | L9110S VCC(VM) | 모터가 쓰는 전원 |
| 모터 전원 접지 | 배터리팩 - | L9110S GND | 모터 전원(-) |
| 공통 접지(필수) | ESP32 GND | L9110S GND | 기준점 공유(안 하면 오작동) |
| 방향/속도 제어 1 | ESP32 GPIO25 | L9110S A-IA | PWM/LOW로 속도·방향 결정 |
| 방향/속도 제어 2 | ESP32 GPIO26 | L9110S A-IB | PWM/LOW로 속도·방향 결정 |
| 모터 구동 출력 | L9110S OA1 | TT모터 단자 1 | 모터로 전력 출력 |
| 모터 구동 출력 | L9110S OA2 | TT모터 단자 2 | 모터로 전력 출력 |

### 연결 체크 포인트
- 모터 방향이 반대면: **OA1 ↔ OA2** (모터선 2가닥) 바꾸기  
- 모터가 안 돌면: **공통접지(GND)** 먼저 확인  
- 낮은 속도에서 안 돌면: 모터는 **기동 임계값**이 있어 너무 낮으면 정지처럼 보일 수 있음  

---

## 핀맵 연결표

### 1) ESP32 ↔ L9110S (A채널)
| ESP32 | L9110S | 역할 |
|---|---|---|
| GPIO2 | A-IA | 방향/속도 제어 입력 1 (PWM 가능) |
| GPIO4 | A-IB | 방향/속도 제어 입력 2 (PWM 가능) |
| GND | GND | 공통 접지(필수) |
| (배터리 +) | VCC(VM) | 모터 전원 입력 |
| (배터리 -) | GND | 모터 전원(-) |

### 2) TT모터 ↔ L9110S (A채널 출력)
| 부품 | 핀/선 이름 | 연결 대상 | 역할 |
|---|---|---|---|
| TT DC모터 | 모터선 1 (색상 상관 X) | L9110S OA1 | 모터 전력 입력 |
| TT DC모터 | 모터선 2 (색상 상관 X) | L9110S OA2 | 모터 전력 입력 |
| L9110S | OA1 / OA2 | TT모터 2가닥 | A채널 모터 출력단 |

---

## A-IA / A-IB 신호에 따른 동작  

| A-IA | A-IB | 모터 동작(예시) | 설명 |
|---|---|---|---|
| 0(LOW) | 0(LOW) | 정지(코스트) | 힘을 풀고 멈춤 |
| PWM(HIGH) | 0(LOW) | 정방향 | A-IA가 PWM이면 속도 조절됨 |
| 0(LOW) | PWM(HIGH) | 역방향 | A-IB가 PWM이면 속도 조절됨 |
| PWM(HIGH) | PWM(HIGH) | 비추천 | 두 쪽 모두 구동하면 제어가 불안정/의도와 다를 수 있음 (수업에서는 피하기) |

> (두 입력 모두 0이면 모터에 힘을 안 주고 관성으로 멈추는 느낌)
> (두 입력 모두 HIGH면 모터에 힘을 주어 브레이크로 멈추는 느낌)
---

## 핀 선택 주의 (GPIO2 / GPIO4 말고 다른 핀을 사용해도 되나?)
- **가능은 하지만 주의가 필요**합니다. 보드/부팅 설정(스트랩 핀)과 관련된 핀을 사용하면 연결 상태에 따라 **부팅이 불안정**해질 수 있습니다.  
- 수업/실습용으로는 **GPIO 핀과 같은 입출력 핀을 쓰는 편이 안정적입니다.

---

## 코드 파일 목록
- **실습 1:** `lab1_forward_reverse_stop.py`  
- **실습 2:** `lab2_pwm_3step_speed.py`  
- **실습 2-1:** `lab2_1_pwm_min_start_test.py`  
- **실습 3:** `lab3_pwm_ramp_up_down.py`  

---

# 실습 1) 정·역·정지 (기본 방향 제어)

## 1) 코드 전체 흐름(큰 그림)
- PWM 핀 준비: IA/IB를 PWM으로 설정  
- 함수 3개 만들기: `stop()`, `forward(speed)`, `reverse(speed)`  
- 반복 실행: 정방향 → 정지 → 역방향 → 정지  

## 2) 주요 코드 분석(짧게)
- `IA/IB` 중 **한쪽만 PWM**을 주고, 다른 한쪽은 **0(LOW)** 로 두면 방향이 결정됨  
- `speed(0~1023)` 값이 클수록 빨라짐  
- `freq=20000(20kHz)`는 모터 “삐—” 소리를 줄이는 용도  

## 3) 코드 (lab1_forward_reverse_stop.py)
```python
from machine import Pin, PWM
import time

# [설정]
IA = PWM(Pin(25), freq=20000)  # A-IA
IB = PWM(Pin(26), freq=20000)  # A-IB

# [핵심 함수 3개]
def stop():
    IA.duty(0)
    IB.duty(0)

def forward(speed):      # speed: 0~1023
    IB.duty(0)
    IA.duty(speed)

def reverse(speed):
    IA.duty(0)
    IB.duty(speed)

print("[실습1] 정·역·정지")
while True:
    print("FWD")
    forward(900); time.sleep(3)

    print("STOP")
    stop(); time.sleep(1)

    print("REV")
    reverse(900); time.sleep(3)

    print("STOP")
    stop(); time.sleep(1)
```

---

# 실습 2) PWM 속도 3단 (LOW / MID / HIGH)

## 1) 코드 전체 흐름(큰 그림)
- 정방향만 유지(한쪽은 0 고정)  
- `LOW → MID → HIGH → STOP` 순서로 반복  
- “PWM 듀티값(duty)” 변화로 속도가 변하는 걸 확인  

## 2) 주요 코드 분석(짧게)
- `IA.duty(값)`이 “모터에 주는 힘(세기)”  
- **LOW/MID에서 안 도는 경우**: 모터가 출발하려면 최소 힘이 필요(기동 임계값) → 값을 더 올리면 해결 → 추후 2-1 실습 참고
- 실전 팁: 실습 2-1로 “내 모터의 최소 출발 PWM”을 먼저 찾고, 그 값보다 조금 크게 LOW를 잡으면 성공률이 높음

## 3) 코드 (lab2_pwm_3step_speed.py)
```python
from machine import Pin, PWM
import time

IA = PWM(Pin(25), freq=20000)  # A-IA
IB = PWM(Pin(26), freq=20000)  # A-IB

def stop():
    IA.duty(0)
    IB.duty(0)

def forward(speed):  # 0~1023
    IB.duty(0)
    IA.duty(speed)

print("[실습2] PWM 속도 3단")
while True:
    print("LOW (약 30%)")
    forward(350); time.sleep(3)

    print("MID (약 60%)")
    forward(650); time.sleep(3)

    print("HIGH (100%)")
    forward(1023); time.sleep(3)

    print("STOP")
    stop(); time.sleep(2)
```

---

# 실습 2-1) 최소 기동 PWM 찾기 (안 도는 이유 확인)

## 1) 코드 전체 흐름(큰 그림)
- PWM 값을 낮은 값부터 조금씩 올림  
- “언제부터 모터가 돌아가기 시작하는지” 관찰  
- 이 값을 기준으로 실습 2의 LOW/MID를 조정  

## 2) 주요 코드 분석(짧게)
- 모터는 **정지 마찰 + 기동전류** 때문에 “최소 출발 힘”이 필요  
- 그래서 LOW가 너무 낮으면 **코드는 맞아도** 모터가 안 도는 것처럼 보임  

## 3) 코드 (lab2_1_pwm_min_start_test.py)
```python
from machine import Pin, PWM
import time

IA = PWM(Pin(25), freq=20000)
IB = PWM(Pin(26), freq=20000)

def forward(speed):
    IB.duty(0)
    IA.duty(speed)

print("[실습2-1] 최소 기동 PWM 찾기")
for s in range(0, 1024, 50):
    print("PWM =", s)
    forward(s)
    time.sleep(2)

# 끝나면 정지
IA.duty(0)
IB.duty(0)
print("DONE")
```

---

# 실습 3) 가속·감속 램프 (부드럽게 속도 변화)

## 1) 코드 전체 흐름(큰 그림)
- PWM 값을 0→1023으로 서서히 올려 가속  
- 잠깐 유지(HOLD)  
- 1023→0으로 서서히 내려 감속
- “부드러운 속도 변화(램프)” 체감  
> ( 이때도 처음값이나 최종값을 2-1실습 값을 참고하여 작성하면 불필요한 계산은 하지 않아도 됨)

## 2) 주요 코드 분석(짧게)
- `for` 문으로 PWM을 조금씩 바꾸면 속도가 계단처럼 변함  
- `time.sleep(0.05)`를 줄이면 더 빠르게 변하고, 늘리면 더 천천히 변함  

## 3) 코드 (lab3_pwm_ramp_up_down.py)
```python
from machine import Pin, PWM
import time

IA = PWM(Pin(25), freq=20000)
IB = PWM(Pin(26), freq=20000)

def stop():
    IA.duty(0)
    IB.duty(0)

def forward(speed):
    IB.duty(0)
    IA.duty(speed)

print("[실습3] 가속·감속 램프")
while True:
    print("RAMP UP")
    for s in range(0, 1024, 40):
        forward(s)
        time.sleep(0.05)

    print("HOLD")
    forward(1023)
    time.sleep(2)

    print("RAMP DOWN")
    for s in range(1023, -1, -40):
        forward(s)
        time.sleep(0.05)

    print("STOP")
    stop()
    time.sleep(2)
```

---

## 자주 발생하는 문제 3가지 (빠른 체크)
1) 모터가 아예 안 돎 → **공통 GND** 먼저 확인(ESP32 GND = L9110S GND = 배터리 -)  
2) LOW/MID에서 안 돎 → **기동 임계값** 때문에 PWM 값을 더 올리기(실습 2-1로 찾기)  
3) 역방향이 약함 → 배터리 전압 저하/접점 불량/모터 편차가 흔함(배터리 새것, 배선 단단히)  
