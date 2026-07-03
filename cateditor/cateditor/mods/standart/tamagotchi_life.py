import tkinter as tk
from tkinter import messagebox
import random

def register_plugin(app):
    # Официальный плагин симулятора жизни для проекта Cat Editor PRO.
    app.tamagotchi_active = True
    app.cheat_god_mode = False
    app.blackout_active = False
    
    # --- РЕСУРСЫ И СТАТИСТИКА КОТА ---
    app.stat_hunger = 100.0
    app.stat_thirst = 100.0
    app.stat_energy = 100.0
    app.stat_fun = 100.0
    app.stat_hygiene = 100.0
    app.stat_poop = 0.0
    app.stat_age = 0.0
    app.cat_status = "Котёнок"
    app.cat_coins = 50
    app.cat_inventory = []
    
    # --- ОБНОВЛЕНИЕ: НАСТРОЕНИЕ И УСТАЛОСТЬ ---
    app.stat_mood = 100.0      # Настроение кота (0 - грустный, 100 - счастливый)
    app.stat_fatigue = 0.0     # Усталость кота (0 - бодрый, 100 - вымотан)
    
    # --- СИСТЕМА ЭЛЕКТРИЧЕСТВА ---
    app.stat_power = 100.0
    app.has_solar_panel = False
    app.active_furniture_bonus = {"energy_save": 0, "fun_save": 0}
    
    # --- ИНТЕРФЕЙС GUI (ВЕРХНЯЯ ПАНЕЛЬ СТАТУСОВ) ---
    app.stats_frame = tk.Frame(app.root, bg="#000000")
    app.stats_frame.pack(side="top", fill="x", pady=2)
    
    app.lbl_hunger = tk.Label(app.stats_frame, text="", font=("Arial", 8, "bold"), bg="#000000", fg="#ff5555")
    app.lbl_hunger.pack(side="left", padx=2)
    app.lbl_thirst = tk.Label(app.stats_frame, text="", font=("Arial", 8, "bold"), bg="#000000", fg="#5555ff")
    app.lbl_thirst.pack(side="left", padx=2)
    app.lbl_energy = tk.Label(app.stats_frame, text="", font=("Arial", 8, "bold"), bg="#000000", fg="#55ff55")
    app.lbl_energy.pack(side="left", padx=2)
    app.lbl_fun = tk.Label(app.stats_frame, text="", font=("Arial", 8, "bold"), bg="#000000", fg="#ff55ff")
    app.lbl_fun.pack(side="left", padx=2)
    
    # Добавляем новые лейблы на панель статусов
    app.lbl_mood = tk.Label(app.stats_frame, text="", font=("Arial", 8, "bold"), bg="#000000", fg="#ffaaee")
    app.lbl_mood.pack(side="left", padx=2)
    app.lbl_fatigue = tk.Label(app.stats_frame, text="", font=("Arial", 8, "bold"), bg="#000000", fg="#ffff55")
    app.lbl_fatigue.pack(side="left", padx=2)
    
    app.lbl_hygiene = tk.Label(app.stats_frame, text="", font=("Arial", 8, "bold"), bg="#000000", fg="#55ffff")
    app.lbl_hygiene.pack(side="left", padx=2)
    app.lbl_poop = tk.Label(app.stats_frame, text="", font=("Arial", 8, "bold"), bg="#000000", fg="#aa5500")
    app.lbl_poop.pack(side="left", padx=2)
    
    app.lbl_power = tk.Label(app.stats_frame, text="", font=("Arial", 8, "bold"), bg="#000000", fg="#ffaa00")
    app.lbl_power.pack(side="left", padx=2)
    
    app.lbl_age = tk.Label(app.stats_frame, text="", font=("Arial", 8, "bold"), bg="#000000", fg="#ffffff")
    app.lbl_age.pack(side="right", padx=5)
    app.lbl_shop_coins = tk.Label(app.stats_frame, text="", font=("Arial", 8, "bold"), bg="#000000", fg="#ffff55")
    app.lbl_shop_coins.pack(side="right", padx=5)
    
    def update_stats_ui():
        app.lbl_hunger.config(text=f"Еда:{int(app.stat_hunger)}%")
        app.lbl_thirst.config(text=f"Вод:{int(app.stat_thirst)}%")
        app.lbl_energy.config(text=f"Сон:{int(app.stat_energy)}%")
        app.lbl_fun.config(text=f"Игр:{int(app.stat_fun)}%")
        app.lbl_mood.config(text=f"Дух:{int(app.stat_mood)}%")
        app.lbl_fatigue.config(text=f"Уст:{int(app.stat_fatigue)}%")
        app.lbl_hygiene.config(text=f"Душ:{int(app.stat_hygiene)}%")
        app.lbl_poop.config(text=f"Лот:{int(app.stat_poop)}%")
        app.lbl_power.config(text=f" Ток:{int(app.stat_power)}%")
        app.lbl_age.config(text=f"⏳{app.cat_status}({app.stat_age:.1f}д)")
        app.lbl_shop_coins.config(text=f"{app.cat_coins}")
        
    def apply_power_theme(is_dark):
        bg_color = "#121212" if is_dark else "#000000"
        panel_bg = "#1a1a1a" if is_dark else "#2d2d2d"
        app.root.configure(bg=bg_color)
        if hasattr(app, 'label'): app.label.configure(bg=bg_color)
        app.stats_frame.configure(bg=bg_color)
        app.actions_frame.configure(bg=panel_bg)
        app.lbl_power.configure(fg="#ff5555" if is_dark else "#ffaa00")
        
    def trigger_random_event():
        if not app.tamagotchi_active or getattr(app, 'cheat_god_mode', False): return
        events = [
            ("Замыкание", "Кот перегрыз кабель питания!\n-25% электричества.", "power_drop"),
            ("Удачная охота", "Кот нашёл за диваном заначку монет!\n+40 монет.", "find_coins"),
            ("Генеральная уборка", "Робот-пылесос напугал кота.\n-20% сна.", "scared_cat"),
            ("Посылка", "Доставлена коробка с рыбой!\n+1 Супер-Сёмга in инвентарь.", "free_loot"),
            ("Тыгыдык", "Кот перевернул лоток! Лоток полон (+100%).", "poop_disaster")
        ]
        title, text, effect_type = random.choice(events)
        if effect_type == "power_drop": app.stat_power = max(0, app.stat_power - 25)
        elif effect_type == "find_coins": app.cat_coins += 40
        elif effect_type == "scared_cat": app.stat_energy = max(0, app.stat_energy - 20)
        elif effect_type == "free_loot": app.cat_inventory.append("Супер-Сёмга")
        elif effect_type == "poop_disaster": app.stat_poop = 100
        messagebox.showinfo(f" Событие: {title}", text)
        update_stats_ui()
        
    # --- ФУНКЦИИ ЖИЗНИ И СОХРАНЕНИЯ (Интеграция с cat_storage) ---
    def save_game():
        if not app.tamagotchi_active: return
        try:
            import os, json
            os.makedirs("catlive", exist_ok=True)
            data = {
                "hunger": app.stat_hunger,
                "thirst": app.stat_thirst,
                "energy": app.stat_energy,
                "fun": app.stat_fun,
                "hygiene": app.stat_hygiene,
                "poop": app.stat_poop,
                "age": app.stat_age,
                "coins": app.cat_coins,
                "status": app.cat_status,
                "inventory": app.cat_inventory,
                "inv": app.cat_inventory, 
                "power": getattr(app, 'stat_power', 100.0),
                "solar": getattr(app, 'has_solar_panel', False),
                "hunt": getattr(app, 'cat_hunt_skill', 1),
                "agility": getattr(app, 'cat_agility', 1),
                "room": getattr(app, 'cat_room_built', {}),
                "bonus": app.active_furniture_bonus,
                # Сохраняем новые параметры
                "mood": app.stat_mood,
                "fatigue": app.stat_fatigue
            }
            with open("catlive/save.catlive", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception:
            pass
            
    def life_ticker_loop():
        if not hasattr(app, 'label') or not app.label.winfo_exists() or not app.tamagotchi_active: return
        
        if getattr(app, 'cheat_god_mode', False):
            app.stat_poop = 0
            app.stat_power = 100
            app.stat_mood = 100.0
            app.stat_fatigue = 0.0
            update_stats_ui()
            app.root.after(1000, life_ticker_loop)
            return
            
        energy_drain = max(0.1, 0.4 - (app.active_furniture_bonus.get("energy_save", 0) * 0.1))
        app.stat_hunger = max(0, app.stat_hunger - 0.4)
        app.stat_thirst = max(0, app.stat_thirst - 0.5)
        app.stat_energy = max(0, app.stat_energy - energy_drain)
        app.stat_fun = max(0, app.stat_fun - 0.3)
        app.stat_hygiene = max(0, app.stat_hygiene - 0.2)
        
        # Динамика Настроения и Усталости в реальном времени
        if app.stat_hunger < 20.0 or app.stat_thirst < 20.0 or app.stat_energy < 20.0:
            app.stat_mood = max(0.0, app.stat_mood - 1.2)
            app.stat_fatigue = min(100.0, app.stat_fatigue + 1.0)
        else:
            app.stat_mood = min(100.0, app.stat_mood + 0.4)
            app.stat_fatigue = max(0.0, app.stat_fatigue - 0.2)
            
        if getattr(app, 'has_solar_panel', False):
            app.stat_power = min(100, app.stat_power + 0.5)
            
        if app.stat_power > 0:
            if app.blackout_active:
                app.blackout_active = False
                apply_power_theme(False)
            if "Авто-лоток 3000" in app.cat_inventory and app.stat_poop > 0:
                app.stat_poop = max(0, app.stat_poop - 5)
                app.stat_power = max(0, app.stat_power - 0.8)
            if "Робот-пылесос" in app.cat_inventory and app.stat_hygiene < 100:
                app.stat_hygiene = min(100, app.stat_hygiene + 1)
                app.stat_power = max(0, app.stat_power - 0.5)
        else:
            if not app.blackout_active:
                app.blackout_active = True
                apply_power_theme(True)
                messagebox.showwarning("Блэкаут", "В доме отключили электричество!")
                
        app.stat_hunger, app.stat_thirst, app.stat_energy = round(app.stat_hunger, 1), round(app.stat_thirst, 1), round(app.stat_energy, 1)
        app.stat_fun, app.stat_hygiene, app.stat_power = round(app.stat_fun, 1), round(app.stat_hygiene, 1), round(app.stat_power, 1)
        app.stat_mood, app.stat_fatigue = round(app.stat_mood, 1), round(app.stat_fatigue, 1)
        
        app.stat_age += 1 / 60
        if app.stat_age >= 10.0: app.cat_status = "Мудрый кот"
        elif app.stat_age >= 5.0: app.cat_status = "Взрослый кот"
        elif app.stat_age >= 2.0: app.cat_status = "Подросток"
        
        if app.stat_poop >= 100:
            app.stat_hygiene, app.stat_poop = 0, 0
            messagebox.showwarning("Ой-ёй!", "Лоток переполнен! Кот устроил беспорядок.")
            
        update_stats_ui()
        if random.random() < 0.015: trigger_random_event()
        save_game()
        app.root.after(1000, life_ticker_loop)
        
    # --- ДЕЙСТВИЯ С КОТОМ (С ФУНКЦИЕЙ СООБЩЕНИЙ) ---
    def feed_cat_realtime():
        app.stat_hunger = min(100, app.stat_hunger + 30)
        app.stat_poop = min(100, app.stat_poop + 10)
        app.stat_mood = min(100, app.stat_mood + 10)
        update_stats_ui()
        messagebox.showinfo("Кормление", "Кот с удовольствием покушал паштет! ")

    def water_cat_realtime():
        app.stat_thirst = min(100, app.stat_thirst + 40)
        app.stat_poop = min(100, app.stat_poop + 5)
        update_stats_ui()
        messagebox.showinfo("Питье", "Кот полакал свежую воду. ")

    def sleep_cat_realtime():
        app.stat_energy = min(100, app.stat_energy + 50)
        app.stat_fatigue = max(0, app.stat_fatigue - 40)
        update_stats_ui()
        messagebox.showinfo("Сон", "Кот лёг на бочок и сладко спит... ")

    def play_cat_realtime():
        if app.stat_fatigue > 80.0 or app.stat_mood < 15.0:
            messagebox.showwarning("Отказ кота", "Котик слишком устал или недоволен! Он залез под диван и отказывается играть.")
            return
        app.stat_fun = min(100, app.stat_fun + 35)
        app.stat_energy = max(0, app.stat_energy - 15)
        app.stat_fatigue = min(100, app.stat_fatigue + 25)
        update_stats_ui()
        messagebox.showinfo("Игры", "Ты поиграл с котиком лазерной указкой! ")

    def wash_cat_realtime():
        app.stat_hygiene = min(100, app.stat_hygiene + 50)
        update_stats_ui()
        messagebox.showinfo("Душ", "Кот чистый и пушистый! ")

    def clean_toilet_realtime():
        app.stat_poop = 0
        update_stats_ui()
        messagebox.showinfo("Уборка", "Лоток идеально очищен! ")

    def recharge_power_grid():
        if app.cat_coins < 15:
            messagebox.showerror("Энергосеть", "Не хватает 15 монет для ручной зарядки!")
            return
        app.cat_coins -= 15
        app.stat_power = 100
        update_stats_ui()
        messagebox.showinfo("Энергосеть", "Энергосеть успешно заряжена на 100%! ")

    # --- ХАКЕРСКАЯ МИНИ-ИГРА ---
    def start_hacking_game():
        if getattr(app, 'stat_power', 100) <= 0:
            messagebox.showerror("Нет питания", "Ноутбук не включается! Сеть обесточена.")
            return
        hack_win = tk.Toplevel(app.root)
        hack_win.title("CatHack Terminal v1.0")
        hack_win.geometry("380x260")
        hack_win.configure(bg="#050505")
        hack_win.resizable(False, False)
        
        target_code = "".join([random.choice(["0", "1"]) for _ in range(6)])
        tk.Label(hack_win, text="(СИСТЕМА ДИСТАНЦИОННОГО ВЗЛОМА)", fg="#00ff00", bg="#050505", font=("Courier", 10, "bold")).pack(pady=10)
        tk.Label(hack_win, text=f"Код обхода брандмауэра:\n{target_code}", fg="#00ff00", bg="#050505", font=("Courier", 12, "bold")).pack(pady=10)
        
        entry_code = tk.Entry(hack_win, font=("Courier", 14), bg="#111111", fg="#ffff00", justify="center")
        entry_code.pack(pady=10, padx=20, fill="x")
        entry_code.focus_set()
        
        def check_hack():
            if entry_code.get().strip() == target_code:
                app.stat_power = max(0, app.stat_power - 15)
                reward = random.randint(60, 160)
                app.cat_coins += reward
                app.stat_fun = min(100, app.stat_fun + 25)
                messagebox.showinfo("УСПЕХ", f"Взлом успешен!\nПереведено на счёт: +{reward} монет.")
                hack_win.destroy()
                update_stats_ui()
                save_game()
            else:
                messagebox.showerror("ОТКАЗ В ДОСТУПЕ", "Неверный код!")
                hack_win.destroy()
                
        tk.Button(hack_win, text="(ЗАПУСТИТЬ ЭКСПЛОЙТ)", bg="#003300", fg="#00ff00", font=("Courier", 10, "bold"), command=check_hack).pack(pady=10)

    # --- СИСТЕМА СОХРАНЕНИЯ И ЗАГРУЗКИ ---
    def load_game():
        try:
            import os, json
            save_path = "catlive/save.catlive"
            if os.path.exists(save_path):
                with open(save_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                app.stat_hunger = data.get("hunger", 100.0)
                app.stat_thirst = data.get("thirst", 100.0)
                app.stat_energy = data.get("energy", 100.0)
                app.stat_fun = data.get("fun", 100.0)
                app.stat_hygiene = data.get("hygiene", 100.0)
                app.stat_poop = data.get("poop", 0.0)
                app.stat_age = data.get("age", 0.0)
                app.cat_coins = data.get("coins", 50)
                app.cat_status = data.get("status", "Котёнок")
                app.cat_inventory = data.get("inventory", data.get("inv", []))
                app.stat_power = data.get("power", 100.0)
                app.has_solar_panel = data.get("solar", False)
                app.cat_hunt_skill = data.get("hunt", 1)
                app.cat_agility = data.get("agility", 1)
                app.cat_room_built = data.get("room", {})
                app.active_furniture_bonus = data.get("bonus", {"energy_save": 0, "fun_save": 0})
                app.stat_mood = data.get("mood", 100.0)
                app.stat_fatigue = data.get("fatigue", 0.0)
        except Exception:
            pass

    # --- ИНВЕНТАРЬ ---
    def open_inventory():
        inv_win = tk.Toplevel(app.root)
        inv_win.title("Рюкзак Кота")
        inv_win.geometry("280x300")
        inv_win.configure(bg="#222222")
        if not app.cat_inventory:
            tk.Label(inv_win, text="Рюкзак пуст", bg="#222222", fg="gray").pack(pady=50)
            return
            
        def use_item(name):
            if name in ("Рыбка", "Супер-Сёмга", " Супер-Корм", "Золотая рыбка", "Золотая рыбка "):
                app.stat_hunger = min(100, app.stat_hunger + 40)
                app.stat_mood = min(100, app.stat_mood + 15)
                if name in app.cat_inventory: app.cat_inventory.remove(name)
            elif name in ("Молоко", " Сливки 20%"):
                app.stat_thirst = min(100, app.stat_thirst + 45)
                if name in app.cat_inventory: app.cat_inventory.remove(name)
            elif name == "Хакерский Ноутбук":
                start_hacking_game()
                inv_win.destroy()
                return
            else:
                messagebox.showinfo("Инвентарь", f"{name} активирован и работает пассивно!")
                return
            update_stats_ui()
            save_game()
            inv_win.destroy()
            open_inventory()
            
        for item in set(app.cat_inventory):
            count = app.cat_inventory.count(item)
            tk.Button(inv_win, text=f"{item} x{count}", bg="#333333", fg="white", command=lambda i=item: use_item(i)).pack(fill="x", padx=10, pady=3)

    # --- КОНСОЛЬ РАЗРАБОТЧИКА (ЧИТЫ) ---
    def open_cheat_console():
        if not app.tamagotchi_active: return
        cheat_win = tk.Toplevel(app.root)
        cheat_win.title("Консоль разработчика")
        cheat_win.geometry("260x120")
        cheat_win.configure(bg="#1c1c1c")
        cheat_win.resizable(False, False)
        tk.Label(cheat_win, text="Введите чит-код:", fg="#00ff00", bg="#1c1c1c", font=("Arial", 9, "bold")).pack(pady=5)
        code_entry = tk.Entry(cheat_win, font=("Courier", 12), bg="#2d2d2d", fg="#ffff00", justify="center")
        code_entry.pack(pady=5, padx=10, fill="x")
        code_entry.focus_set()
        
        def apply_cheat():
            cheat = code_entry.get().strip().lower()
            if cheat == "catcoins":
                app.cat_coins += 999
                messagebox.showinfo("Чит", "Добавлено +999 монет!")
            elif cheat == "fullstats":
                app.stat_hunger, app.stat_thirst, app.stat_energy, app.stat_fun, app.stat_hygiene, app.stat_power = 100, 100, 100, 100, 100, 100
                app.stat_poop = 0
                app.stat_mood = 100.0
                app.stat_fatigue = 0.0
                messagebox.showinfo("Чит", "Все статы восстановлены!")
            elif cheat == "godmode":
                app.cheat_god_mode = not getattr(app, 'cheat_god_mode', False)
                status = "ВКЛЮЧЕН" if app.cheat_god_mode else "ВЫКЛЮЧЕН"
                messagebox.showinfo("Чит", f"Режим бога: {status}")
            elif cheat == "fixanim":
                app.blackout_active = False
                if hasattr(app, 'apply_power_theme'): app.apply_power_theme(False)
                if hasattr(app, 'render_cat'): app.render_cat()
                elif hasattr(app, 'draw_cat'): app.draw_cat()
                messagebox.showinfo("Чит", "Попытка перезапустить анимацию ядра успешна!")
            else:
                messagebox.showerror("Ошибка", "Неверный код!")
            cheat_win.destroy()
            update_stats_ui()
            save_game()
            
        tk.Button(cheat_win, text="Активировать", bg="#00aa00", fg="white", command=apply_cheat).pack(pady=5)

    def wrap_action(original_cmd):
        def check_and_save():
            original_cmd()
            save_game()
        return check_and_save

    # --- СУПЕРМАРКЕТ ТОВАРОВ ---
    def open_shop():
        shop_win = tk.Toplevel(app.root)
        shop_win.title("Кошачий Супермаркет")
        shop_win.geometry("360x420")
        shop_win.configure(bg="#222222")
        items = {
            " Еда и Напитки": (("Рыбка", 10, "food"), ("Молоко", 8, "drink"), ("Супер-Сёмга", 35, "food")),
            " Электроника": (("Авто-лоток 3000", 400, "elec_poop"), ("Робот-пылесос", 300, "elec_clean"), ("Хакерский Ноутбук", 600, "elec_hack"), ("Sol-Панель 3000", 350, "elec_solar")),
            " Мебель и Уют": (("Мягкая лежанка", 150, "build_energy"), ("Кошачий комплекс", 250, "build_fun")),
            " Одежда и Оружие": (("Очки PRO", 100, "item_wear"), ("Лазерная указка", 180, "item_weapon"))
        }
        def buy_item(name, price, item_type):
            if app.cat_coins < price:
                # --- Продолжение функции buy_item (Внутри open_shop) ---
                messagebox.showerror("Магазин", "Недостаточно монет!")
                return
            app.cat_coins -= price
            if item_type == "elec_solar":
                app.has_solar_panel = True
                messagebox.showinfo("Магазин", "Sol-Панель успешно установлена на крыше!")
            else:
                app.cat_inventory.append(name)
                messagebox.showinfo("Магазин", f"Успешно куплено: {name}!")
            update_stats_ui()
            save_game()

        # Отрисовка товаров в окне магазина (Внутри open_shop)
        for cat, items_list in items.items():
            tk.Label(shop_win, text=cat, bg="#222222", fg="#ffff55", font=("Arial", 10, "bold")).pack(pady=4)
            for name, price, itype in items_list:
                btn_text = f"{name} ({price})"
                tk.Button(shop_win, text=btn_text, bg="#444444", fg="white", 
                          command=lambda n=name, p=price, t=itype: buy_item(n, p, t)).pack(fill="x", padx=15, pady=2)

    # --- ПАНЕЛЬ КНОПОК ДЕЙСТВИЙ В ГЛАВНОМ GUI ---
    app.actions_frame = tk.Frame(app.root, bg="#2d2d2d")
    app.actions_frame.pack(side="bottom", fill="x", ipady=2)


    def hunt_action_wrapper():
        if app.stat_fatigue > 75.0 or app.stat_mood < 20.0:
            messagebox.showwarning("Отказ кота", "Котик слишком устал или недоволен, чтобы идти на Охоту!")
            return
        if hasattr(app, 'start_hunt_game'):
            app.start_hunt_game()
        else:
            messagebox.showinfo("Охота", "Кот ушёл ловить мышей!")

    btns = [
        ("Корм", "#522", wrap_action(feed_cat_realtime)),
        ("Вода", "#225", wrap_action(water_cat_realtime)),
        ("Сон", "#552", wrap_action(sleep_cat_realtime)),
        ("Игра", "#525", wrap_action(play_cat_realtime)),
        ("Душ", "#255", wrap_action(wash_cat_realtime)),
        ("Лоток", "#333", wrap_action(clean_toilet_realtime)),
        ("Ток", "#770", wrap_action(recharge_power_grid)),
        ("Охота", "#252", wrap_action(hunt_action_wrapper)),
        ("Шоп", "#c5a000", open_shop),
        ("Инв", "#444", open_inventory)
    ]

    for text, color, cmd in btns:
        tk.Button(app.actions_frame, text=text, bg=color, fg="white", font=("Arial", 8, "bold"), command=cmd).pack(side="left", padx=1, expand=True, fill="x")

    # Привязка чит-консоли на тильду
    app.root.bind("<grave>", lambda event: open_cheat_console())

    # Первичный запуск систем мода
    load_game()
    update_stats_ui()
    life_ticker_loop()

    return True
