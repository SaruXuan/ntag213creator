# -*- coding: utf-8 -*-
# 蜂鳴器短腳 --- 兩個電阻並聯(紅紅棕+橘橘棕) --- GND
# 蜂鳴器長腳 --- GPIO 18 (Pin #12)

from time import sleep
import RPi.GPIO as GPIO

PIN_BUZZER = 18     # GPIO 18 = pin #12
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_BUZZER, GPIO.OUT)

def alert(times,F,T,pin,interval):
    for t in range(times):
        buzzer = GPIO.PWM(pin, F)   # (pin,frequency)
        buzzer.start(50)            # 佔空比 -> 影響PWM訊號出來的電壓 -> 可能影響音量?
        sleep(T)                    # 發聲的時間長度
        buzzer.stop()
        sleep(interval)
    
def SND_connected():
    alert(1,2093,0.1,PIN_BUZZER,0.05)
    alert(1,3136,0.1,PIN_BUZZER,0.05)
    alert(1,4186,0.1,PIN_BUZZER,0)

def SND_disconnected():
    alert(1,523,0.1,PIN_BUZZER,0.05)
    alert(1,494,0.3,PIN_BUZZER,0)

def SND_cardDetect():
    alert(1,1500,0.08,PIN_BUZZER,0.05)
    alert(1,1500,0.08,PIN_BUZZER,0.05)

# SND_cardDetect()
# GPIO.cleanup()