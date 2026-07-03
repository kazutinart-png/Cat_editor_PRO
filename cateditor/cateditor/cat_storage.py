import os
import json
import importlib.util
import sys

MODS_DIR = "./mods"
STANDART_DIR = "./mods/standart"
CATS_DIR = "./mods/cats"

DEFAULT_CATS = {
    "Ушастый кот": [
        " ( \\_ / ) \n ( ='.'= ) \n ( )_( ) ",
        " ( \\_ / ) \n ( =^.^= ) \n ( )_( ) "
    ],
    "Bongo Cat": [
        " /\\_ /\\ \n( ='.'=) \n( ~ , ~)🐾",
        " /\\_ /\\ \n( =^.^=) \n🐾(~ , ~) "
    ],
    "Nyan Cat": [
        "~_~_~_~_ /\\_ /\\\n_~_~_~_ ( o . o)\n~_~_~_~  \"\"   \"\"",
        "_~_~_~_  /\\_ /\\\n~_~_~_~ ( o . o)\n_~_~_~_  \"\"   \"\""
    ]
}

def init_storage():
    for directory in [MODS_DIR, STANDART_DIR, CATS_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)

def load_all_cats():
    init_storage()
    cats = DEFAULT_CATS.copy()
    if os.path.exists(CATS_DIR):
        for filename in os.listdir(CATS_DIR):
            if filename.endswith(".cat"):
                cat_name = filename[:-4]
                filepath = os.path.join(CATS_DIR, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, list) and len(data) >= 2:
                            cats[cat_name] = data
                except Exception:
                    pass
    return cats

def save_cat_mod(name, frame1, frame2):
    init_storage()
    for char in ['/', '\\', '?', '%', '*', ':', '|', '"', '<', '>']:
        name = name.replace(char, '')
    if not name:
        return False, "Недопустимое имя!"
    filepath = os.path.join(CATS_DIR, f"{name}.cat")
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump([frame1, frame2], f, ensure_ascii=False, indent=4)
        return True, filepath
    except Exception as e:
        return False, str(e)

def delete_cat_mod(cat_name):
    filepath = os.path.join(CATS_DIR, f"{cat_name}.cat")
    if os.path.exists(filepath):
        os.remove(filepath)

def load_plugins(app_instance):
    """Сканирует и загружает плагины исключительно из папки ./mods/standart/"""
    init_storage()
    plugins = []
    
    if STANDART_DIR not in sys.path:
        sys.path.append(STANDART_DIR)
        
    if os.path.exists(STANDART_DIR):
        for filename in os.listdir(STANDART_DIR):
            if filename.endswith(".py"):
                mod_name = filename[:-3]
                filepath = os.path.join(STANDART_DIR, filename)
                try:
                    spec = importlib.util.spec_from_file_location(mod_name, filepath)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    if hasattr(module, "register_plugin"):
                        # Запрашиваем метаданные плагина без передачи инстанса приложения
                        if hasattr(module, "get_permissions"):
                            req_perms = module.get_permissions()
                        else:
                            req_perms = []
                            
                        # Передаем плагин в контроллер разрешений GUI
                        if app_instance.verify_plugin_permissions(mod_name, req_perms):
                            plugin_info = module.register_plugin(app_instance)
                            if plugin_info:
                                plugins.append(plugin_info)
                except Exception as e:
                    print(f"Ошибка загрузки плагина {filename}: {e}")
    return plugins
