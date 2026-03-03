# [실습1] IR 센서 디지털 값 읽기
# 배선: AO -> GPIO26, VCC -> 3V3, GND -> GND

from machine import Pin
import time

IR_PIN = 26
ir = Pin(IR_PIN, Pin.IN)

print("[실습1] IR 디지털 값 읽기 시작 (반전 출력)")
print("출력 기준: 검은색=0, 흰색=1")

while True:
    raw = ir.value()      # 원래 센서 출력 (검은색=1, 흰색=0)
    print("IR =", raw)    
    # 값을 반대로 출력하고 싶다면 , val = 1- raw , print("IR =", val) 으로 추가/변경 해주세요!
    time.sleep(0.1)

