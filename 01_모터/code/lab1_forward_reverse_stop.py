from machine import Pin, PWM
import time

# [설정]
IA = PWM(Pin(2), freq=20000)  # A-IA
IB = PWM(Pin(4), freq=20000)  # A-IB

# [핵심 함수 3개]
def stop():
    IA.duty(0); IB.duty(0)

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
