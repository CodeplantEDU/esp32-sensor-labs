수위 감지 센서 실습 - (ESP32 + MicroPython/Thonny)

ESP32 + 수위 감지 센서 + RGB LED를 이용해 물의 높이를 측정하고, 수위 상태에 따라 LED 색상으로 경고를 보내는 실습 세트입니다.

실습 목표

ESP32의 ADC(아날로그 입력) 기능을 활용해 수위 센서의 전도 원리를 이해하고, 조건문(if-else)을 통해 수위 단계별로 초록(안전) → 파랑(주의) → 빨강(위험) LED를 제어할 수 있다.

강의 자료 요약 (슬라이드 핵심)

수위 센서의 정의: 물의 높이나 존재 여부를 감지해 누수나 수위를 판단하는 센서 (Slide 3)

동작 원리: 전극 패턴이 물에 직접 닿아 변화하는 **저항(전도성)**을 측정합니다. 물에 많이 잠길수록 저항이 감소하고 출력값은 커집니다. (Slide 7~9)

센서 특징: 보드형 센서는 아날로그(AO) 값을 출력하여 대략적인 수위를 연속적인 값으로 확인할 수 있습니다. (Slide 11~13)

준비물

ESP32(DevKit)

수위 감지 센서(접촉식 보드형)

RGB LED (공통 음극/Common Cathode 권장)

점퍼선 (M-F, M-M)

브레드보드

배선(핀 연결)

수위 센서:

ESP32 GPIO34 → 센서 SIG (S)

ESP32 3.3V → 센서 VCC (+)

ESP32 GND → 센서 GND (-)

RGB LED:

ESP32 GPIO25 → LED R (Red)

ESP32 GPIO26 → LED G (Green)

ESP32 GPIO27 → LED B (Blue)

ESP32 GND → LED GND (가장 긴 핀)

회로 연결표 (ESP32 + 센서 + RGB LED)

핵심: 수위 센서는 아날로그 신호를 내보내므로 반드시 ESP32의 ADC 지원 핀에 연결해야 합니다.

연결 목적

출발(부품/핀)

도착(부품/핀)

설명(한 줄)

센서 전원

ESP32 3.3V

수위 센서 VCC

센서 동작 전원

신호 입력

수위 센서 SIG

ESP32 GPIO34

수위에 따른 아날로그 값 전달

LED 빨강 제어

ESP32 GPIO25

RGB LED R

위험(High) 상태 표시

LED 초록 제어

ESP32 GPIO26

RGB LED G

안전(Low) 상태 표시

LED 파랑 제어

ESP32 GPIO27

RGB LED B

주의(Mid) 상태 표시

공통 접지

ESP32 GND

센서/LED GND

회로 기준점 공유

수위 센서 값에 따른 동작  

수위 값(0~4095)

상태 판정

LED 색상

설명

0 ~ 500

안전(LOW)

초록색 (G)

물이 없거나 매우 낮은 상태

500 ~ 1800

주의(MID)

파랑색 (B)

물이 중간 정도 차오른 상태

1800 이상

위험(HIGH)

빨강색 (R)

물이 넘칠 위험이 있는 상태

(측정값은 물의 순도나 센서 상태에 따라 다르므로 실습 2-1을 통해 본인만의 기준값을 찾아야 합니다.)

코드 파일 목록

실습 1: lab1_water_raw_read.py (실시간 수위 모니터링)

실습 2: lab2_water_level_alert.py (3단계 LED 경보)

실습 2-1: lab2_1_find_threshold.py (임계값 찾기 테스트)

실습 1) 아날로그 수위 값 읽기

1) 코드 전체 흐름

ADC 설정: GPIO34번을 12비트(0~4095) 아날로그 입력으로 설정

반복 실행: 0.1초마다 현재 수위 센서 값을 읽어 출력

2) 코드 (lab1_water_raw_read.py)

from machine import Pin, ADC
import time

# [설정]
water_adc = ADC(Pin(34))
water_adc.atten(ADC.ATTN_11DB) # 0~3.6V 범위까지 측정 가능하도록 설정

print("[실습1] 수위 값 읽기 시작")
while True:
    val = water_adc.read()
    print("현재 수위 값:", val)
    time.sleep(0.1)


실습 2) 수위에 따른 3색 LED 제어

1) 코드 전체 흐름

수위 값을 읽어 if-elif-else 조건문으로 구간을 나눔

각 구간에 해당하는 RGB LED 핀만 켜고 나머지는 끔

2) 코드 (lab2_water_level_alert.py)

from machine import Pin, ADC
import time

# [핀 설정]
water_adc = ADC(Pin(34))
water_adc.atten(ADC.ATTN_11DB)

led_r = Pin(25, Pin.OUT)
led_g = Pin(26, Pin.OUT)
led_b = Pin(27, Pin.OUT)

def all_off():
    led_r.value(0); led_g.value(0); led_b.value(0)

print("[실습2] 수위별 LED 경보 시스템")
while True:
    val = water_adc.read()
    all_off() # 이전 색상 초기화
    
    if val < 500:
        led_g.value(1) # 초록색
        status = "SAFE"
    elif val < 1800:
        led_b.value(1) # 파랑색
        status = "WARNING"
    else:
        led_r.value(1) # 빨강색
        status = "DANGER"
        
    print(f"Value: {val} | Status: {status}")
    time.sleep(0.5)


자주 발생하는 문제 3가지 (빠른 체크)

값이 계속 0인 경우: 센서의 VCC와 GND 배선을 확인하고, SIG 핀이 GPIO34에 제대로 꽂혔는지 확인하세요.

LED 색상이 섞임: all_off() 함수가 매 루프마다 호출되는지 확인하여 이전 LED가 꺼졌는지 체크하세요.

센서 부식 주의: 실습이 끝나면 센서 표면의 물기를 깨끗이 닦아주어야 전극 부식을 막을 수 있습니다.

본 가이드는 CODEPLANT 교육 자료를 바탕으로 작성되었습니다.
