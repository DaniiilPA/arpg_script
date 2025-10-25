import time
import keyboard

class BaseScript:

    def __init__(self, delay=0.5, func=None, comb="", block_key=""):

        self.delay = delay
        self.last_press = 0
        self.func = func
        self.is_pressed = False
        self.comb = comb
        self.block_key = block_key
        self.is_stopped = False
        
        try:
            self.block_hotkey = keyboard.add_hotkey(self.block_key, self.block_status)
            print(f"инициализация прошла успешно, блокировка: {self.block_key}")
        except ValueError as e:
            print(f"ошибка при инициализации: {e}")
        
       
    def debounce(self):
        cur_time = time.time()
       
        if cur_time - self.last_press >= self.delay:
            self.func()
            self.last_press = cur_time

        else:
            print(f"еще не прошло {self.delay}")
            
    def block_status(self):
        if not self.is_pressed:
            print(f"включена блокировка для {self.__class__.__name__}, {self.block_key} чтобы отключить") if not self.is_stopped else print(f"выключена блокировка для {self.__class__.__name__}, {self.block_key} чтобы включить")
            self.is_stopped = not self.is_stopped
        else: print(f"выключите скрипт на {self.comb}")
            
        
        
        
        
        
            
    