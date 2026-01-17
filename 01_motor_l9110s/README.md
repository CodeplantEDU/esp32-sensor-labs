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
