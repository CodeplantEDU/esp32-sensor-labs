# 01. 모터드라이버(L9110S) - 실습 1

## 실습 제목
- 정·역·정지

## 0) 한 줄 목표
ESP32가 L9110S에 신호를 줘서 모터를 **정방향 → 정지 → 역방향 → 정지**로 반복시키는 실습

## 준비물
- ESP32(DevKit)
- L9110S 모터드라이버
- TT모터 1개
- AA 배터리팩(4개 = 6V 권장)
- 점퍼선

## 배선(모터 A채널)
- GPIO25 → A-IA
- GPIO26 → A-IB
- 모터선 2개 → OA1 / OA2
- 배터리(+) → VCC
- 배터리(-) → GND
- ESP32 GND → L9110S GND (**공통접지 필수**)

---

## 1) 코드 파일
- `lab1_forward_reverse_stop.py`

---

## 2) 코드 전체 흐름(큰 그림)
1. PWM 준비: 모터 속도 조절 가능한 신호를 만들 준비  
2. 기능 3개 만들기: `stop()`, `forward(speed)`, `reverse(speed)`  
3. 반복 실행: `while True`로 계속 “정 → 정지 → 역 → 정지” 반복  

---

## 3) 주요 코드 분석

---

### (1) 모듈(도구) 불러오기
- `Pin` : ESP32의 핀(전기 신호 출력) 제어
- `PWM` : 속도 조절용 PWM 신호 생성
- `time.sleep()` : 동작 사이에 기다리기(초 단위)

```python
from machine import Pin, PWM
import time
(2) PWM 출력 핀 설정
GPIO25 → A-IA, GPIO26 → A-IB

freq=20000 (20kHz) : 모터에서 나는 ‘삐—’ 소리를 줄이기 좋은 주파수

IA = PWM(Pin(25), freq=20000)  # A-IA
IB = PWM(Pin(26), freq=20000)  # A-IB
(3) 핵심 함수 3개
1) stop() : 정지(코스트)
A-IA=0, A-IB=0

힘을 풀고 멈추는 느낌(관성으로 살짝 굴러갈 수 있음)

def stop():
    IA.duty(0)
    IB.duty(0)
2) forward(speed) : 정방향 + 속도
A-IB=0, A-IA=PWM(speed)

speed 값이 클수록 더 빠르게 회전 (범위: 0~1023)

def forward(speed):  # 0~1023
    IB.duty(0)
    IA.duty(speed)
3) reverse(speed) : 역방향 + 속도
A-IA=0, A-IB=PWM(speed)

정방향과 반대로 회전

def reverse(speed):
    IA.duty(0)
    IB.duty(speed)
(4) 반복 실행(루프)
정방향 3초 → 정지 1초 → 역방향 3초 → 정지 1초를 계속 반복

while True:
    forward(900); time.sleep(3)
    stop(); time.sleep(1)
    reverse(900); time.sleep(3)
    stop(); time.sleep(1)
(5) 체크 포인트(자주 막히는 곳)
모터가 안 돌면: GND 공통(ESP32 GND ↔ L9110S GND ↔ 배터리 -) 먼저 확인

낮은 속도에서 안 돌면: 모터는 기동에 필요한 최소 힘(임계값) 이 있어서 값이 너무 낮으면 정지처럼 보일 수 있음
