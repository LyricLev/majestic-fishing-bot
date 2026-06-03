import time
import pyautogui

print("Скрипт запущен. Наводи мышку на нужные точки экрана.")
print("Каждые 3 секунды скрипт будет выводить текущие координаты курсора.")
print("Для выхода нажмите Ctrl+C в консоли.\n")

try:
    while True:
        x, y = pyautogui.position()
        print(f"Текущие координаты мыши: X = {x}, Y = {y}")
        time.sleep(3)
except KeyboardInterrupt:
    print("\nМониторинг завершен.")