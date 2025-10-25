from logic import Key_Scripter, Key_Togler, keyboard
import json

def load_config_params(filename='params.json'):
    """
    Загружает конфигурацию из файла и возвращает два словаря с параметрами.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            full_config = json.load(f)
            
        params_A = full_config.get("script", {})
        params_B = full_config.get("togler", {})
        
        return params_A, params_B
            
    except FileNotFoundError:
        print(f"{filename} не найден")
        return {}, {}
    except json.JSONDecodeError:
        print(f"ошибка формата в {filename}")
        return {}, {}


if __name__ == "__main__":

    params_sc, params_to = load_config_params()
    keyscript = Key_Scripter(**params_sc)
    keytogl = Key_Togler(**params_to)
    keyboard.wait("f12")
    keyboard.unhook_all()
    
