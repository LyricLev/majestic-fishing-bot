import time
import random
import json
import cv2
import numpy as np
import pydirectinput
from PIL import ImageGrab

# Загрузка настроек
with open('config.json', 'r') as f:
    config = json.load(f)

def human_delay(min_t, max_t):
    """Случайная пауза для имитации действий человека"""
    time.sleep(random.uniform(min_t, max_t))

def check_zone():
    """Снимок триггер-зоны и проверка наличия целевого цвета"""
    bbox = config["trigger_zone"]
    # Захват указанной области экрана
    screen = np.array(ImageGrab.grab(bbox=bbox))
    img_bgr = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    
    # Фильтр по цвету (например, зеленый бегунок)
    low_color = np.array(config["target_color_hsv_low"])
    high_color = np.array(config["target_color_hsv_high"])
    
    mask = cv2.inRange(hsv, low_color, high_color)
    # Если количество пикселей нужного цвета выше порога
    return np.sum(mask) > 5000

def play_game():
    print("[Бот] Обнаружена поклёвка! Начинаю прожимание...")
    human_delay(0.15, 0.3)  # Тайминг реакции человека
    
    start_time = time.time()
    # Прожимаем клавишу в течение 4 секунд (стандартное время мини-игры)
    while time.time() - start_time < 4.0:
        pydirectinput.keyDown(config["minigame_key"])
        time.sleep(random.uniform(0.04, 0.1))
        pydirectinput.keyUp(config["minigame_key"])
        time.sleep(random.uniform(0.05, 0.12))

def main():
    print("[Бот] Скрипт готов. Переключитесь на окно с игрой.")
    print("[Бот] Старт через 5 секунд...")
    time.sleep(5)
    
    while True:
        print("[Бот] Забрасываю удочку...")
        pydirectinput.press(config["cast_key"])
        human_delay(2.0, 3.0)  # Ожидание завершения анимации заброса
        
        bite = False
        search_start = time.time()
        
        # Ждем поклёвку максимум 40 секунд
        while time.time() - search_start < 40:
            if check_zone():
                bite = True
                break
            time.sleep(config["check_delay"])
            
        if bite:
            play_game()
            human_delay(4.0, 6.0)  # Пауза после поимки рыбы
        else:
            print("[Бот] Время ожидания истекло, перезаброс...")
            human_delay(1.0, 2.0)

if __name__ == "__main__":
    main()