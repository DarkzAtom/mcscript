from pynput.keyboard import Key, Controller as KeyboardController, Listener as KeyboardListener
from pynput.mouse import Button, Controller as MouseController
import time
import random
import threading

keyboard = KeyboardController()
mouse = MouseController()
button1_key = Key.shift_l
delay = random.uniform(10, 20)
key_pressed = False
start_key = ']'
stop_key = Key.enter
script_thread = None

def script():
    global key_pressed, delay, script_thread
    while key_pressed:
        keyboard.press(button1_key)
        keyboard.press('d')
        click_thread = threading.Thread(target=smooth_click, args=(delay,))
        move_thread = threading.Thread(target=smooth_move, args=(-15, 0, delay))
        click_thread.start()
        move_thread.start()
        # if key_pressed == False:
        #     break
        move_thread.join()
        click_thread.join()
        keyboard.release(button1_key)
        keyboard.release('d')
        keyboard.press(button1_key)
        keyboard.press('a')
        move_thread = threading.Thread(target=smooth_move, args=(15, 0, delay))
        click_thread = threading.Thread(target=smooth_click, args=(delay,))
        click_thread.start()
        move_thread.start()
        # if key_pressed == False:
        #     break
        move_thread.join()
        click_thread.join()
        keyboard.release(button1_key)
        keyboard.release('a')
def smooth_move(xm, ym, t):
    start_time = time.time()
    end_time = start_time + t
    while time.time() < end_time:
        mouse.move(xm, ym)
        time.sleep(1 / 60)

def smooth_click(t):
    start_time = time.time()
    end_time = start_time + t
    while time.time() < end_time:
        mouse.press(Button.left)
        mouse.release(Button.left)
        time.sleep(1 / 6)
def on_press(key):
    global key_pressed, script_thread
    try:
        if key.char == start_key:
            key_pressed = True
            print('Script running')
            script_thread = threading.Thread(target=script)
            script_thread.start()
    except AttributeError:
        pass

def on_release(key):
    global key_pressed, script_thread
    if key == stop_key:
        key_pressed = False
        threading.Thread(keyboard.release('a'))
        threading.Thread(keyboard.release('d'))
        threading.Thread(keyboard.release(Key.shift_l))
        print('Script stopped')
        return False

with KeyboardListener(on_press=on_press, on_release=on_release) as listener:
    listener.join()