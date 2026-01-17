# 모터드라이버(L9110S) - 실습 1, 실습 2, 실습 2-1, 실습 3

## 실습 목표
ESP32가 L9110S에 신호를 줘서 모터를 **정방향 → 정지 → 역방향 → 정지**로 제어하고,  
PWM으로 **속도(세기)**를 조절할 수 있다.

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
- 낮은 속도에서 안 돌면: 모터는 **기동 임계값**이 있어 너무 낮으면 정지처럼 보일 수 있음

---

# 1) 코드 파일 목록
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

## 2) 주요 코드 분석
### (1) 모듈(도구) 불러오기
- `Pin` : ESP32 핀 제어
- `PWM` : PWM 신호 생성(속도 조절)
- `time.sleep()` : 시간 지연

```python
from machine import Pin, PWM
import time
(2) PWM 출력 핀 설정
GPIO25 → A-IA, GPIO26 → A-IB

freq=20000(20kHz) : 모터 ‘삐—’ 소리를 줄이기 좋음

IA = PWM(Pin(25), freq=20000)  # A-IA
IB = PWM(Pin(26), freq=20000)  # A-IB
(3) 핵심 함수 3개
stop() : IA=0, IB=0 → 코스트 정지(힘 풀고 멈춤)

forward(speed) : IB=0, IA=PWM → 정방향

reverse(speed) : IA=0, IB=PWM → 역방향

def stop():
    IA.duty(0); IB.duty(0)

def forward(speed):      # 0~1023
    IB.duty(0)
    IA.duty(speed)

def reverse(speed):
    IA.duty(0)
    IB.duty(speed)
(4) 반복 실행(루프)
정방향 3초 → 정지 1초 → 역방향 3초 → 정지 1초 반복

while True:
    forward(900); time.sleep(3)
    stop(); time.sleep(1)
    reverse(900); time.sleep(3)
    stop(); time.sleep(1)
실습 2) PWM 속도 3단 (LOW/MID/HIGH)
1) 코드 전체 흐름(큰 그림)
forward(speed) 함수로 정방향 유지

PWM duty를 3단계로 바꿔서 속도 차이를 확인

LOW→MID→HIGH→STOP 반복

2) 주요 코드 분석
(1) 핵심 포인트
duty(값)이 작으면 모터가 안 움직일 수도 있음
(기동 임계값 때문에 LOW가 “정지처럼” 보일 수 있음)

(2) 속도 3단 구조
print("[실습2] PWM 속도 3단")
while True:
    print("LOW")
    forward(700); time.sleep(3)

    print("MID")
    forward(850); time.sleep(3)

    print("HIGH")
    forward(1023); time.sleep(3)

    print("STOP")
    stop(); time.sleep(3)
실습 2-1) 최소 기동 PWM 찾기 (모터가 도는 최소값)
1) 코드 전체 흐름(큰 그림)
PWM 값을 조금씩 올리면서

“언제부터 모터가 실제로 도는지” 최소값을 찾기

그 값보다 낮으면 LOW에서 안 도는 이유를 설명 가능

2) 주요 코드 분석
(1) 테스트 방법(학생용)
숫자를 올리다가 “처음 움직이는 순간” 값 기록

print("[실습2-1] 최소 기동 PWM 찾기")
for s in range(0, 1024, 50):
    print("speed =", s)
    forward(s)
    time.sleep(1)
stop()
실습 3) PWM 가속·감속 램프 (부드럽게 속도 변화)
1) 코드 전체 흐름(큰 그림)
PWM 값을 0→1023으로 서서히 증가(가속)

잠깐 유지

1023→0으로 서서히 감소(감속)

모터가 “부드럽게” 변하는 걸 확인

2) 주요 코드 분석
(1) 램프 업/다운 구조
print("[실습3] 가속·감속 램프")
while True:
    print("RAMP UP")
    for s in range(0, 1024, 40):
        forward(s)
        time.sleep(0.05)

    print("HOLD")
    forward(1023); time.sleep(2)

    print("RAMP DOWN")
    for s in range(1023, -1, -40):
        forward(s)
        time.sleep(0.05)

    print("STOP")
    stop(); time.sleep(2)
자주 발생하는 질문(짧게)
Q. LOW에서 모터가 왜 안 돌아요?
→ 모터는 **처음 움직이려면 더 큰 힘(기동전류/임계 PWM)**이 필요해서, 낮은 duty는 정지처럼 보일 수 있어요.

Q. 역방향이 더 느린 느낌이 나요.
→ 모터/기어/마찰 편차 + 배터리 상태 + 드라이버 출력 차이로 방향별 속도가 달라질 수 있어요.
