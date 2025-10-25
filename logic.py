import keyboard
from base import BaseScript
import time
import threading


class MacrosError(ValueError):
    def __init__(self, l1, l2):
        self.l1 = l1
        self.l2 = l2
        
        full_massage = f"Списки должны быть одинаковой длины, длина переданных списков: {self.l1}, {self.l2}"
        
        super().__init__(full_massage)  
        
        
class Key_Togler(BaseScript):
    def __init__(self, comb="f8", key="w", delay=0.5, block_key="f10"):
        
        self.key = Key_Togler.splitter(key)
        
        super().__init__(delay=delay, func=self.toggle_key_state, comb=comb, block_key=block_key)        
        
        
        try:
            self.hotkey = keyboard.add_hotkey(self.comb, self.debounce)
            print(f"инициализация прошла успешно комбинация: {self.comb} клавиши: {' '.join(self.key)}")
        except ValueError as e:
            print(f"ошибка при инициализации: {e}")
    
    def toggle_key_state(self):
            
        self.is_pressed = not self.is_pressed
        
        
        if self.is_stopped == False:
            func = keyboard.press if self.is_pressed else keyboard.release  
                
            for key in self.key:
                func(key)
                print(f"зажата {key}") if self.is_pressed else print(f"отжата {key}")
        else:
            print(f"заблокировано")
            self.is_pressed = not self.is_pressed

            
    @staticmethod
    def splitter(key):
        return key.lower().replace(" ", "").split("+")


class Key_Scripter(BaseScript):
    
    def __init__(self, comb="f9", key_list=[], delay_list=[], delay=0.5, block_key="f11"):
        
        self.validate(key_list, delay_list)
        
        self.key_list = key_list
        self.delay_list = delay_list
        self.macrothread = None
        
        
        super().__init__(delay=delay, func=self.key_script, comb=comb, block_key=block_key)

        try:
            self.hotkey = keyboard.add_hotkey(self.comb, self.thread_start_stop)
            print(f"инициализация прошла успешно комбинация: {self.comb} клавиши: {self.key_list} задержки: {self.delay_list}")
        except ValueError as e:
            print(f"ошибка при инициализации: {e}")

    def thread_start_stop(self):
        self.is_pressed = not self.is_pressed
        
        if self.is_pressed and not self.is_stopped:
            print(f"старт")
            self.macrothread = threading.Thread(target=self.key_script)
            self.macrothread.daemon = True
            self.macrothread.start()
        else:
            if not self.is_stopped:
                print(f"стоп") 
            else: 
                print(f"заблокировано")
                self.is_pressed = not self.is_pressed
    
    
    def key_script(self):        
        
        while self.is_pressed:
            for key, delay in zip(self.key_list, self.delay_list):
                if not self.is_pressed:
                    break
                keyboard.send(key)
                time.sleep(delay)
            
            if self.is_pressed and not self.key_list:
                time.sleep(0.01)

    def validate(self, l1, l2):
        lenght1, lenght2 = len(l1), len(l2)
        
        if lenght1 != lenght2:
            
            raise MacrosError(lenght1, lenght2)
        
         
if __name__ == "__main__":


    keyscript = Key_Scripter(comb="f9", key_list=["i", "o", "i", "o", "i"], delay_list=[1, 1, 1, 1, 1], block_key="f12")
    keytogl = Key_Togler(comb="f8", key="q+w", delay=0.5, block_key="f11")
    keyboard.wait("esc")
    keyboard.unhook_all()
