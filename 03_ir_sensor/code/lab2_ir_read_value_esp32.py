# [실습1] IR 센서 아날로그 값 읽기
# 배선: AO -> GPIO26, VCC -> 3V3, GND -> GND

from machine import Pin, ADC
import time

IR_PIN = 26
adc = ADC(Pin(IR_PIN))

# ESP32 ADC 설정 (권장)
try:
    adc.atten(ADC.ATTN_11DB)     # 0 ~ 약 3.3V 측정
    adc.width(ADC.WIDTH_12BIT)   # 12bit 해상도 (0~4095)
except:
    pass

print("[실습1] IR 아날로그 값 읽기 시작")
print("범위: 0 ~ 4095 (값이 클수록 반사 강함)")

while True:
    try:
        val = adc.read()        # MicroPython ESP32 (0~4095)
    except:
        val = adc.read_u16()    # 일부 보드 (0~65535)

    print("IR =", val)
    time.sleep(0.1)
