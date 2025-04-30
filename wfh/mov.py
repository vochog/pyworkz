
import pyautogui
import time
import math
import random

# safety feature - moving mouse to corner will abort the program
pyautogui.FAILSAFE = True

def move_mouse():
    # Get screen size
    screen_width, screen_height = pyautogui.size()

    # Move mouse in circular pattern 
    for i in range(0, 360, 10):
        x = screen_width // 4 + math.cos(math.radians(i)) * 100
        y = screen_height // 2 + math.sin(math.radians(i)) * 100

        # Move mouse to position 
        pyautogui.moveTo(x, y, duration=0.25)
        time.sleep(0.1)

def scroll_down():
    # Scroll down 3 times
    for _ in range(3):
        pyautogui.scroll(-100) # Negative value scrolls down
        time.sleep(0.5)

def ctrl_tab():
    # Press alt+Tab to switch windows
    pyautogui.keyDown('ctrl')
    time.sleep(1)
    pyautogui.press('tab')
    # time.sleep(0.2)
    pyautogui.keyUp('ctrl')
    print("Ctrl+Tab pressed - switched window")

# def alt_tab():
#     # Press alt+Tab to switch windows
#     pyautogui.keyDown('alt')
#     time.sleep(1)
#     pyautogui.press('tab')
#     # time.sleep(0.2)
#     pyautogui.keyUp('alt')
#     print("Alt+Tab pressed - switched window")

def main():
    print("Script started. Move mouse to top-left corner to abort.")
    try:
        while True:
            print("Moving mouse...")
            move_mouse()

            print("Scrolling down...")
            scroll_down()

            # Randomly Alt+Tab every 1-5 minutes (optional)
            if random.randint(1, 10) > 5: # -30% chance per cycle
                ctrl_tab()

            print("Waiting 30 secconds...")
            time.sleep(30)
    except pyautogui.FailSafeException:
        print("Fail-safe triggered (mouse moved to corner). Exciting...")

if __name__ == "__main__":
    main()
