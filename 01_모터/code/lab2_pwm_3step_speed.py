from machine import Pin, PWM
import time

IA = PWM(Pin(2), freq=20000)
IB = PWM(Pin(4), freq=20000)

def stop():
    IA.duty(0); IB.duty(0)

def forward(speed):
    IB.duty(0)
    IA.duty(speed)

print("[실습2] PWM 속도 3단")
while True:
    print("LOW (30%)")
    forward(650); time.sleep(3)

    print("MID (60%)")
    forward(850); time.sleep(3)

    print("HIGH (100%)")
    forward(1023); time.sleep(3)

    print("STOP")
    stop(); time.sleep(2)

