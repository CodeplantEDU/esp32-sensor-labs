# 모터드라이버(L9110S) - 실습 1, 실습 2, 실습 2-1, 실습 3

## 실습 목표
ESP32가 L9110S에 신호를 줘서 모터를 **정방향 → 정지 → 역방향 → 정지**로 제어하고, PWM으로 **속도(세기)**를 조절할 수 있다.

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
- ESP32 **GPIO25** → L9110S **A-IA**
- ESP32 **GPIO26** → L9110S **A-IB**
- TT모터 선 2개 → L9110S **OA1 / OA2**
- 배터리(+) → L9110S **VCC(VM)**
- 배터리(-) → L9110S **GND**
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
- 낮은 속도에서 안 돌면: 모터는 **기동 임계값**이 있어 너무 낮으면 정지처럼 보일 수 있음(→ 실습 2-1 참고)

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

## 2) 주요 코드 분석 (한 문단/끊김 방지 버전)
### (1) 모듈(도구) 불러오기
- `Pin` : ESP32의 핀(전기 신호 출력) 제어  
- `PWM` : 속도 조절용 PWM 신호 생성  
- `time.sleep()` : 동작 사이 기다리기(초 단위)

```python
from machine import Pin, PWM
import time
(2) PWM 출력 핀 설정
GPIO25 → A-IA, GPIO26 → A-IB

freq=20000(20kHz): 모터 ‘삐—’ 소리(가청음) 줄이기

IA = PWM(Pin(25), freq=20000)  # A-IA
IB = PWM(Pin(26), freq=20000)  # A-IB
(3) 핵심 함수 3개
stop() : A-IA=0, A-IB=0 → 힘 풀고 멈춤(코스트)

forward(speed) : A-IB=0, A-IA=PWM → 정방향

reverse(speed) : A-IA=0, A-IB=PWM → 역방향

def stop():
    IA.duty(0)
    IB.duty(0)

def forward(speed):      # speed: 0~1023
    IB.duty(0)
    IA.duty(speed)

def reverse(speed):
    IA.duty(0)
    IB.duty(speed)
(4) 반복 실행(루프)
정방향 3초 → 정지 1초 → 역방향 3초 → 정지 1초 반복

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
실습 2) PWM 속도 3단 (LOW / MID / HIGH)
1) 코드 전체 흐름(큰 그림)
forward(speed)만 사용해서 속도만 3단계로 바꿔보기

LOW → MID → HIGH → STOP 반복

2) 주요 코드 분석 (한 문단/끊김 방지 버전)
(1) 핵심 아이디어
PWM의 duty() 값이 클수록 모터에 전달되는 “평균 힘”이 커져서 더 빠르게 돈다.

단, 모터는 기동 임계값이 있어서 너무 낮으면 “안 도는 것처럼” 보일 수 있다.

LOW/MID는 현장에서 잘 도는 값으로 조정하는 것을 추천한다.

(2) 코드 (3단 속도)
from machine import Pin, PWM
import time

IA = PWM(Pin(25), freq=20000)
IB = PWM(Pin(26), freq=20000)

def stop():
    IA.duty(0)
    IB.duty(0)

def forward(speed):      # 0~1023
    IB.duty(0)
    IA.duty(speed)

print("[실습2] PWM 속도 3단")
while True:
    print("LOW")
    forward(450); time.sleep(3)   # 필요하면 500~650로 올려보기

    print("MID")
    forward(750); time.sleep(3)

    print("HIGH")
    forward(1023); time.sleep(3)

    print("STOP")
    stop(); time.sleep(2)
실습 2-1) “최소 기동 PWM” 찾기 (내 모터는 몇부터 돌까?)
1) 코드 전체 흐름(큰 그림)
PWM 값을 아주 낮은 값부터 조금씩 올리면서

모터가 “처음으로 움직이는 값(기동 임계값)”을 찾는다.

이 값을 알면 실습 2에서 LOW/MID 범위를 더 현실적으로 잡을 수 있다.

2) 주요 코드 분석 (한 문단/끊김 방지 버전)
(1) 핵심 아이디어
모터는 “처음 돌기 위한 최소 힘(기동 임계값)”이 필요하다.

임계값 아래에서는 PWM을 줘도 정지처럼 보일 수 있다.

(2) 코드 (임계값 찾기)
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

print("[실습2-1] 최소 기동 PWM 찾기")
stop(); time.sleep(1)

for s in range(0, 1024, 50):   # 0, 50, 100, ... 1000
    print("PWM =", s)
    forward(s)
    time.sleep(2)

stop()
print("DONE")
실습 3) PWM 램프 (서서히 가속/감속)
1) 코드 전체 흐름(큰 그림)
PWM을 0 → 1023까지 천천히 올려서 가속

잠깐 유지(HOLD)

1023 → 0으로 천천히 내려서 감속

마지막에 STOP

2) 주요 코드 분석 (한 문단/끊김 방지 버전)
(1) 핵심 아이디어
for문으로 PWM 값을 조금씩 바꾸면 “서서히” 속도가 변한다.

급가속/급감속 대신, 자연스러운 속도 변화(램프)를 만든다.

(2) 코드 (램프)
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
    for s in range(0, 1024, 40):   # 0 -> 1023
        forward(s)
        time.sleep(0.05)

    print("HOLD")
    forward(1023)
    time.sleep(2)

    print("RAMP DOWN")
    for s in range(1023, -1, -40): # 1023 -> 0
        forward(s)
        time.sleep(0.05)

    print("STOP")
    stop()
    time.sleep(2)
자주 발생하는 문제(한 번에 해결)
모터가 아예 안 돎: 배터리(-), L9110S GND, ESP32 GND 공통 접지 확인

LOW/MID에서만 안 돎: 기동 임계값 문제 → 실습 2-1로 최소 PWM 찾기

역방향이 더 약해 보임: 모터/기어박스 편차, 브러시/마찰 차이, 배선 접촉 저항 영향 등으로 발생 가능(정상 범주)
