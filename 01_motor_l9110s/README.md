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

### (1) 모듈(도구) 불러오기
```python
from machine import Pin, PWM
import time
Pin: ESP32 핀 제어

PWM: 속도 조절 신호 생성

time.sleep(): 동작 사이 기다리기

(2) PWM 출력 핀 설정
IA = PWM(Pin(25), freq=20000)  # A-IA
IB = PWM(Pin(26), freq=20000)  # A-IB
GPIO25 → A-IA, GPIO26 → A-IB

freq=20000(20kHz): 모터 소음(삐 소리) 줄이기

(3) 핵심 함수 3개
stop(): 정지
def stop():
    IA.duty(0); IB.duty(0)
A-IA=LOW, A-IB=LOW → 힘 풀고 멈춤(코스트)

forward(speed): 정방향 + 속도
def forward(speed):
    IB.duty(0)
    IA.duty(speed)
A-IB=0, A-IA=PWM → 정방향 회전

reverse(speed): 역방향 + 속도
def reverse(speed):
    IA.duty(0)
    IB.duty(speed)
A-IA=0, A-IB=PWM → 역방향 회전

(4) 반복 실행(루프)
while True:
    forward(900); time.sleep(3)
    stop(); time.sleep(1)
    reverse(900); time.sleep(3)
    stop(); time.sleep(1)
정방향 3초 → 정지 1초 → 역방향 3초 → 정지 1초 반복

4) 체크 포인트(문제 해결)
모터가 안 돌면: 공통접지(GND 연결) 먼저 확인

LOW 속도에서 안 돌면: 시동에 필요한 힘이 부족한 것(기동 임계)


> 포인트: 이 문서에 **표/사진/배선도 이미지**까지 같이 넣으면 학생이 거의 안 헤매.

---

# 6) 레포 맨 위 README.md(목차)도 만들면 더 좋음
레포 최상단 `README.md`에는 “전체 실습 링크”만 넣어.

예시:

```md
# ESP32 센서/모터 실습 자료

## 목차
- [01. 모터드라이버(L9110S)](01_motor_l9110s/)
