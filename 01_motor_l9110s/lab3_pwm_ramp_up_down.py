from machine import Pin, PWM
import time

IA = PWM(Pin(2), freq=20000)
IB = PWM(Pin(4), freq=20000)

def stop():
    IA.duty(0)
    IB.duty(0)

def forward(speed):  # 0~1023
    IB.duty(0)
    IA.duty(speed)

print("[실습3] 가속·감속 램프")

while True:
    print("RAMP UP")
    for s in range(0, 1024, 40):      # 0 -> 1023
        forward(s)
        time.sleep(0.05)

    print("HOLD")
    forward(1023)
    time.sleep(2)

    print("RAMP DOWN")
    for s in range(1023, -1, -40):    # 1023 -> 0
        forward(s)
        time.sleep(0.05)

    print("STOP")
    stop()
    time.sleep(2)

