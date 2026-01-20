from machine import Pin, PWM
import time

IA = PWM(Pin(2), freq=20000)
IB = PWM(Pin(4), freq=20000)

def forward(s):
    IB.duty(0); IA.duty(s)

print("0~1023 올리면서 '처음 움직이는 값' 찾기")
for s in range(0, 1024, 50):
    forward(s)
    print("duty =", s)
    time.sleep(0.6)

