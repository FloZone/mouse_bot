import contextlib
import random
import sys
import time

from infi.systray import SysTrayIcon
import keyboard
import pyautogui

ICON_RUN = "color.ico"
ICON_PAUSE = "grey.ico"
OFFSET_MIN = -150
OFFSET_MAX = 150
DELAY_MIN = 1
DELAY_MAX = 2
KEY_PRESS = "ctrl"
SCREEN_X, SCREEN_Y = pyautogui.size()

SCRIPT_RUN = False
SCRIPT_EXIT = False


def mouse_move_once():
    current_x, current_y = pyautogui.position()
    new_x = current_x + random.randint(OFFSET_MIN, OFFSET_MAX)
    new_y = current_y + random.randint(OFFSET_MIN, OFFSET_MAX)
    if new_x < 0:
        new_x = 0
    if new_x > SCREEN_X:
        new_x = SCREEN_X
    if new_y < 0:
        new_y = 0
    if new_y > SCREEN_Y:
        new_y = SCREEN_Y
    delay = random.uniform(DELAY_MIN, DELAY_MAX)
    pyautogui.moveTo(new_x, new_y, delay, pyautogui.easeOutQuad)


def start_simulate_activity():
    global SCRIPT_RUN

    SCRIPT_RUN = True
    pyautogui.moveTo(SCREEN_X / 2, SCREEN_Y / 2)
    last_event = 0
    while SCRIPT_RUN:
        mouse_move_once()
        now = int(time.time())
        if now - last_event > 5:
            last_event = now
            pyautogui.press(KEY_PRESS)


def stop_simulate_activity():
    global SCRIPT_RUN

    SCRIPT_RUN = False


def mouse_print_position(moving):
    x, y = pyautogui.position()
    status = "▶️" if moving else "■"
    pos = f"X: {str(x).rjust(4)} Y: {str(y).rjust(4)}  {status}"
    print(pos, end="")
    print("\b" * len(pos), end="", flush=True)


def systray_init():
    menu = (("Start", None, systray_start),)
    systray = SysTrayIcon(ICON_PAUSE, "MouseBot", menu, on_quit=systray_stop)
    systray.start()
    return systray


def systray_start(systray):
    systray.update(icon=ICON_RUN)
    start_simulate_activity()


def systray_stop(systray):
    global SCRIPT_EXIT

    SCRIPT_EXIT = True


if __name__ == "__main__":
    print("*** MouseBot🐭 ***\n'esc' to pause bot")
    pyautogui.FAILSAFE = False
    systray = systray_init()
    with contextlib.suppress(KeyboardInterrupt):
        while not SCRIPT_EXIT:
            mouse_print_position(SCRIPT_RUN)
            if keyboard.is_pressed("esc"):
                systray.update(icon=ICON_PAUSE)
                stop_simulate_activity()

    print("")
    systray.shutdown()
    sys.exit(0)
