import time
import pyautogui

# Holds down the alt key
#pyautogui.keyDown("alt")

# Presses the tab key once
#pyautogui.press("tab")

# Lets go of the alt key
#pyautogui.keyUp("alt")

r = 200
i = 1
for x in range(0, r):
    print(i)
    i+=1
    pyautogui.press("up")
    time.sleep(3.9)
