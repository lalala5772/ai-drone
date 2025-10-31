# test_environment.py
import sys
import platform

print("===== Python Environment Check =====")
print(f"Python version : {platform.python_version()}")
print(f"Platform       : {platform.system()} {platform.release()}")
print("====================================\n")

# --- TensorFlow / Keras ---
try:
    import tensorflow as tf
    from tensorflow import keras
    print(f"TensorFlow version : {tf.__version__}")
    print(f"Keras version      : {keras.__version__}")
    print("TensorFlow test ->", "GPU available ✅" if tf.config.list_physical_devices('GPU') else "CPU only ⚠️")
except Exception as e:
    print("❌ TensorFlow/Keras error:", e)

print()

# --- NumPy ---
try:
    import numpy as np
    arr = np.array([[1, 2], [3, 4]])
    print(f"NumPy version : {np.__version__}")
    print("NumPy test -> sum:", np.sum(arr))
except Exception as e:
    print("❌ NumPy error:", e)

print()

# --- OpenCV ---
try:
    import cv2
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.putText(img, "OK", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
    print(f"OpenCV version : {cv2.__version__}")
    print("OpenCV test -> success ✅ (image matrix created)")
except Exception as e:
    print("❌ OpenCV error:", e)

print()

# --- MediaPipe ---
try:
    import mediapipe as mp
    print(f"MediaPipe version : {mp.__version__}")
except Exception as e:
    print("❌ MediaPipe error:", e)

print()

# --- PyAutoGUI ---
try:
    import pyautogui
    print(f"PyAutoGUI version : {pyautogui.__version__}")
    screen_width, screen_height = pyautogui.size()
    print(f"Screen size -> {screen_width}x{screen_height}")
except Exception as e:
    print("❌ PyAutoGUI error:", e)

print()

# --- Keyboard ---
try:
    import keyboard
    print(f"Keyboard module version : {keyboard.__version__}")
    print("Keyboard test -> waiting for key 'q' press (5 sec timeout)")
    import time
    start = time.time()
    pressed = False
    while time.time() - start < 5:
        if keyboard.is_pressed('q'):
            pressed = True
            break
    print("Result ->", "Key detected ✅" if pressed else "No key press detected ⚠️")
except Exception as e:
    print("❌ Keyboard error:", e)

print("\n===== Test Completed =====")
