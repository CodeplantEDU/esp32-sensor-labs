수위 감지 센서 실습 - (ESP32 + MicroPython/Thonny)

ESP32 + 수위 감지 센서 + RGB LED를 이용해 물의 높이를 측정하고, 수위 상태에 따라 LED 색상으로 경고를 보내는 실습 세트입니다.

실습 목표

ESP32의 ADC(아날로그 입력) 기능을 활용해 수위 센서의 값을 읽고, 조건문(if-else)을 통해 수위 단계별로 초록(안전) → 파랑(주의) → 빨강(위험) LED를 제어할 수 있다.

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

ESP32 GND → LED GND (Longest pin)

회로 연결표 (ESP32 + 센서 + LED)

핵심: 수위 센서는 아날로그 신호를 내보내므로 반드시 ESP32의 **ADC 지원 핀(GPIO 32-39)**에 연결해야 합니다.

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

위험 상태 표시

LED 초록 제어

ESP32 GPIO26

RGB LED G

안전 상태 표시

LED 파랑 제어

ESP32 GPIO27

RGB LED B

주의 상태 표시

공통 접지

ESP32 GND

센서/LED GND

회로 기준점 공유

연결 체크 포인트

센서 방향: 전극 패턴이 있는 부분이 물에 닿아야 하며, 회로가 있는 상단은 닿지 않게 주의합니다.

RGB LED 종류: 공통 음극(GND)인지 공통 양극(VCC)인지 확인 후 배선하세요. (본 실습은 음극 기준)

접촉 불량: 아날로그 값은 접촉 상태에 따라 변동이 심하므로 점퍼선을 단단히 고정합니다.

수위 값에 따른 상태 동작 (알고리즘)

수위 값(0~4095)

상태 판정

LED 색상

설명

0 ~ 500

안전(LOW)

초록색 (G)

물이 없거나 매우 낮은 상태

500 ~ 1500

주의(MID)

파랑색 (B)

물이 중간 정도 차오른 상태

1500 이상

위험(HIGH)

빨강색 (R)

물이 넘칠 위험이 있는 상태

(값은 실습 환경의 수질이나 전극 상태에 따라 달라질 수 있으므로 실습 2-1을 통해 보정합니다.)

코드 파일 목록

실습 1: lab1_raw_value_read.py (센서 값 모니터링)

실습 2: lab2_water_level_led.py (수위별 LED 제어)

실습 2-1: lab2_1_threshold_test.py (나만의 임계값 찾기)

실습 1) 아날로그 값 읽기 (기본 모니터링)

1) 코드 전체 흐름

ADC 핀 설정: GPIO34번을 아날로그 입력으로 설정

반복 실행: 0.5초마다 현재 센서 값을 시리얼 모니터에 출력

2) 코드 (lab1_raw_value_read.py)

from machine import Pin, ADC
import time

# [설정] GPIO34핀을 ADC로 설정 (0~4095 범위)
sensor = ADC(Pin(34))
sensor.atten(ADC.ATTN_11DB) # 3.3V까지 읽을 수 있도록 설정

print("[실습1] 수위 값 모니터링 시작")
while True:
    val = sensor.read()
    print("수위 센서 값:", val)
    time.sleep(0.5)


실습 2) 수위별 3색 LED 제어

1) 코드 전체 흐름

센서 값 읽기 → if-else 조건 비교 → 해당하는 LED 핀만 High 전송

안전(Green), 주의(Blue), 위험(Red) 순서로 색상 변화 확인

2) 코드 (lab2_water_level_led.py)

from machine import Pin, ADC
import time

# 핀 설정
water_sensor = ADC(Pin(34))
water_sensor.atten(ADC.ATTN_11DB)

led_r = Pin(25, Pin.OUT)
led_g = Pin(26, Pin.OUT)
led_b = Pin(27, Pin.OUT)

def led_clear():
    led_r.value(0)
    led_g.value(0)
    led_b.value(0)

print("[실습2] 수위 기반 LED 경보 시스템")
while True:
    val = water_sensor.read()
    led_clear()
    
    if val < 500:
        led_g.value(1) # 안전
        print("SAFE", val)
    elif val < 1500:
        led_b.value(1) # 주의
        print("WARNING", val)
    else:
        led_r.value(1) # 위험
        print("DANGER", val)
        
    time.sleep(0.5)


자주 발생하는 문제 3가지 (빠른 체크)

값이 0으로 고정됨: 수위 센서의 VCC/GND가 ESP32와 제대로 연결되었는지 확인하세요.

값이 너무 튐(불안정): 전극 표면의 이물질을 닦아내거나, ESP32의 GND 공통 접지가 잘 되어 있는지 확인하세요.

LED 색상이 이상함: R, G, B 핀 번호가 배선과 일치하는지, 혹은 LED가 공통 양극(Anode) 타입이라 value(0)일 때 켜지는 것인지 확인하세요.

본 가이드는 ESP32와 수위 센서 교육용 자료로 제작되었습니다.
