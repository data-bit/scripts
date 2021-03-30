import time
import pyautogui

pyautogui.FAILSAFE = False

r = 1100
i = 1
for x in range(0, r):
    print(i)
    i+=1
    pyautogui.press("up")
    time.sleep(3.9)