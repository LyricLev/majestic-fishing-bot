import tkinter as tk
import customtkinter as ctk
import threading
import time
import json
# Импортируем функции из твоего прошлого файла bot.py
import pydirectinput
from bot import check_zone, play_game, human_delay

# Настройка внешнего вида (Темная тема)
ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue") 

class BotApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Majestic Fishing Bot v1.0")
        self.geometry("400x400")
        self.resizable(False, False)

        self.is_running = False
        self.bot_thread = None

        # --- Заголовок ---
        self.logo_label = ctk.CTkLabel(self, text="Majestic Fishing", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=20)

        # --- Поля ввода координат ---
        self.coord_frame = ctk.CTkFrame(self)
        self.coord_frame.pack(pady=10, padx=20, fill="x")

        self.coord_label = ctk.CTkLabel(self.coord_frame, text="Настройка зоны триггера (X1, Y1, X2, Y2):")
        self.coord_label.grid(row=0, column=0, columnspan=4, pady=5, padx=10)

        self.entry_x1 = ctk.CTkEntry(self.coord_frame, width=60, placeholder_text="X1")
        self.entry_x1.grid(row=1, column=0, padx=5, pady=5)
        self.entry_y1 = ctk.CTkEntry(self.coord_frame, width=60, placeholder_text="Y1")
        self.entry_y1.grid(row=1, column=1, padx=5, pady=5)
        self.entry_x2 = ctk.CTkEntry(self.coord_frame, width=60, placeholder_text="X2")
        self.entry_x2.grid(row=1, column=2, padx=5, pady=5)
        self.entry_y2 = ctk.CTkEntry(self.coord_frame, width=60, placeholder_text="Y2")
        self.entry_y2.grid(row=1, column=3, padx=5, pady=5)

        # Загрузим дефолтные значения из config.json, если он есть
        self.load_current_config()

        # --- Статус работы ---
        self.status_label = ctk.CTkLabel(self, text="Статус: Остановлен", text_color="red", font=ctk.CTkFont(size=14))
        self.status_label.pack(pady=15)

        # --- Кнопки управления ---
        self.start_button = ctk.CTkButton(self, text="СТАРТ БОТА", fg_color="green", hover_color="darkgreen", command=self.start_bot)
        self.start_button.pack(pady=10, fill="x", padx=40)

        self.stop_button = ctk.CTkButton(self, text="СТОП", fg_color="red", hover_color="darkred", command=self.stop_bot)
        self.stop_button.pack(pady=5, fill="x", padx=40)
        self.stop_button.configure(state="disabled") # Изначально кнопка СТОП выключена

    def load_current_config(self):
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                tz = config.get("trigger_zone", [900, 500, 1020, 580])
                self.entry_x1.insert(0, str(tz[0]))
                self.entry_y1.insert(0, str(tz[1]))
                self.entry_x2.insert(0, str(tz[2]))
                self.entry_y2.insert(0, str(tz[3]))
        except Exception:
            pass

    def save_config_from_gui(self):
        # Обновляем координаты в config.json перед запуском
        try:
            with open('config.json', 'r+') as f:
                config = json.load(f)
                config["trigger_zone"] = [
                    int(self.entry_x1.get()),
                    int(self.entry_y1.get()),
                    int(self.entry_x2.get()),
                    int(self.entry_y2.get())
                ]
                f.seek(0)
                json.dump(config, f, indent=2)
                f.truncate()
        except Exception as e:
            print(f"Ошибка сохранения конфига: {e}")

    def bot_loop(self):
        """Основной цикл бота, работающий в фоновом потоке"""
        with open('config.json', 'r') as f:
            config = json.load(f)

        # Даем время развернуть игру
        for i in range(5, 0, -1):
            if not self.is_running: return
            self.status_label.configure(text=f"Старт через {i} сек... Разверните GTA", text_color="orange")
            time.sleep(1)

        while self.is_running:
            self.status_label.configure(text="Статус: Закидываю удочку...", text_color="green")
            pydirectinput.press(config["cast_key"])
            
            # Имитация паузы с проверкой флага остановки
            for _ in range(30): 
                if not self.is_running: return
                time.sleep(0.1)

            self.status_label.configure(text="Статус: Ожидание поклёвки...", text_color="yellow")
            bite = False
            search_start = time.time()
            
            while time.time() - search_start < 40 and self.is_running:
                if check_zone():
                    bite = True
                    break
                time.sleep(config["check_delay"])
                
            if bite and self.is_running:
                self.status_label.configure(text="Статус: Ловлю рыбу!", text_color="purple")
                play_game()
                human_delay(4.0, 6.0)
            elif not bite and self.is_running:
                self.status_label.configure(text="Статус: Пусто, перезаброс...", text_color="orange")
                human_delay(1.0, 2.0)

    def start_bot(self):
        if not self.is_running:
            self.save_config_from_gui()
            self.is_running = True
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            
            # Запускаем бота в отдельном потоке
            self.bot_thread = threading.Thread(target=self.bot_loop, daemon=True)
            self.bot_thread.start()

    def stop_bot(self):
        if self.is_running:
            self.is_running = False
            self.status_label.configure(text="Статус: Останавливаюсь...", text_color="orange")
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.status_label.configure(text="Статус: Остановлен", text_color="red")

if __name__ == "__main__":
    app = BotApp()
    app.mainloop()