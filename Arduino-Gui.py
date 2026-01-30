import inspect

if not hasattr(inspect, 'getargspec'):
    inspect.getargspec = inspect.getfullargspec

import tkinter as tk
from tkinter import messagebox, Menu
from pyfirmata import Arduino, PWM
from time import sleep

# --- Логика работы с Arduino ---
try:
    # Убедитесь, что порт правильный (например, COM6)
    board = Arduino("COM6")
    board.digital[3].mode = PWM
    board.digital[5].mode = PWM
except Exception as e:
    messagebox.showerror("Ошибка", f"Не удалось подключить Arduino: {e}")
    exit()

# !!! 1. Функция для изменения яркости в реальном времени (для шкалы)
def change_brightness(val):
    brightness = float(val) / 100.0  # Конвертируем 0-100 в 0.0-1.0
    board.digital[3].write(brightness)

# !!! 2. Обновленные функции кнопок
def LedON(event=None):
    LEDbright.set(100) # Ставим шкалу на 100% (сработает change_brightness)

def LedOFF(event=None):
    LEDbright.set(0)   # Ставим шкалу на 0% (сработает change_brightness)

def aboutMsg():
    messagebox.showinfo("Информация", "Версия программы: 2.1\nИсправлен диммер.")

# --- Создание графического интерфейса ---
win = tk.Tk()
win.title("Dimmer LED Control")
win.geometry("300x250")

# Меню
main_menu = Menu(win)
win.config(menu=main_menu)
file_menu = Menu(main_menu, tearoff=0)
file_menu.add_command(label="Выход (Ctrl+Q)", command=win.destroy)
main_menu.add_cascade(label="Файл", menu=file_menu)
help_menu = Menu(main_menu, tearoff=0)
help_menu.add_command(label="О программе", command=aboutMsg)
main_menu.add_cascade(label="Справка", menu=help_menu)

win.columnconfigure(0, weight=1)
win.columnconfigure(1, weight=1)

# Поле ввода времени
tk.Label(win, text="Время задержки (сек):").grid(column=0, row=0, sticky="e", padx=5, pady=5)
LEDtime = tk.Entry(win, bd=3, width=10, justify="center")
LEDtime.insert(0, "0.5")
LEDtime.grid(column=1, row=0, sticky="w", padx=5, pady=5)

# !!! 3. Привязываем команду к шкале
LEDbright = tk.Scale(win, 
                     from_=0, 
                     to=100, 
                     orient=tk.HORIZONTAL, 
                     label="Яркость LED (%)", 
                     tickinterval=25,
                     length=200,
                     command=change_brightness)
LEDbright.set(50) 
LEDbright.grid(column=0, row=1, columnspan=2, padx=10, pady=10)

# Кнопки управления
bluebtn = tk.Button(win, bd=4, text="ВКЛ (Key: 1)", command=LedON, bg="#ddddff")
bluebtn.grid(column=0, row=2, padx=10, pady=10, sticky="ew")

redbtn = tk.Button(win, bd=4, text="ВЫКЛ (Key: 0)", command=LedOFF, bg="#ffdddd")
redbtn.grid(column=1, row=2, padx=10, pady=10, sticky="ew")

# Привязка событий
win.bind('<KeyPress-1>', LedON)
win.bind('<KeyPress-0>', LedOFF)
win.bind('<Control-q>', lambda e: win.destroy())

win.mainloop()