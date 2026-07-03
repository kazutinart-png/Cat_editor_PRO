import tkinter as tk
from tkinter import messagebox
import random
import cat_storage

class CatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Редактор котиков PRO")
        self.root.geometry("550x800")
        
        self.cats = {}
        self.current_frames = []
        self.current_frame_idx = 0
        self.font_size = 20
        self.anim_speed = 300
        self.disco_mode = False
        self.r_val, self.g_val, self.b_val = 185, 204, 96 
        
        # База одобренных разрешений (сохраняется в рамках сессии)
        self.approved_permissions = {}
        
        self.show_main_menu()

    def verify_plugin_permissions(self, plugin_name, permissions):
        """Контроллер разрешений: запрашивает подтверждение у пользователя"""
        if not permissions:
            return True
        if plugin_name in self.approved_permissions:
            return self.approved_permissions[plugin_name]
            
        perm_text = "\n".join([f"- {p}" for p in permissions])
        msg = f"Плагин '{plugin_name}' запрашивает следующие разрешения:\n\n{perm_text}\n\nРазрешить запуск данного плагина?"
        is_allowed = messagebox.askyesno("Контроллер разрешений", msg)
        
        self.approved_permissions[plugin_name] = is_allowed
        return is_allowed

    def get_hex_color(self):
        return f"#{self.r_val:02x}{self.g_val:02x}{self.b_val:02x}"

    def show_main_menu(self):
        self.disco_mode = False
        self.cats = cat_storage.load_all_cats()
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg="#1e1e1e")
        title_label = tk.Label(self.root, text="РЕДАКТОР КОТОВ PRO", font=("Arial", 16, "bold"), fg="#ffffff", bg="#1e1e1e")
        title_label.pack(pady=15)
        
        list_canvas = tk.Canvas(self.root, bg="#1e1e1e", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=list_canvas.yview)
        scroll_frame = tk.Frame(list_canvas, bg="#1e1e1e")
        scroll_frame.bind("<Configure>", lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all")))
        list_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        list_canvas.configure(yscrollcommand=scrollbar.set)
        list_canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")

        for cat_name in self.cats.keys():
            item_frame = tk.Frame(scroll_frame, bg="#1e1e1e", pady=4)
            item_frame.pack(fill="x", expand=True)
            btn = tk.Button(item_frame, text=cat_name, font=("Arial", 11, "bold"), bg="#2d2d2d", fg="#00ff00" if cat_name in cat_storage.DEFAULT_CATS else "#ffff00", width=28, height=2, command=lambda name=cat_name: self.start_animation(name))
            btn.pack(side="left", padx=5)
            if cat_name not in cat_storage.DEFAULT_CATS:
                del_btn = tk.Button(item_frame, text="X", font=("Arial", 10, "bold"), bg="#aa0000", fg="white", width=3, height=2, command=lambda name=cat_name: self.confirm_delete(name))
                del_btn.pack(side="left", padx=5)
                
        # --- НОВЫЙ БЛОК: МОНИТОРИНГ ПЛАГИНОВ ---
        plugins_monitor_frame = tk.LabelFrame(self.root, text="🔌 Активные плагины в сессии", fg="#00ffff", bg="#1e1e1e", font=("Arial", 10, "bold"))
        plugins_monitor_frame.pack(side="bottom", fill="x", padx=20, pady=10)

        # Загружаем плагины для проверки, какие из них активны и одобрены
        active_plugins = []
        for mod_name, allowed in self.approved_permissions.items():
            if allowed:
                active_plugins.append(mod_name)

        if not active_plugins:
            tk.Label(plugins_monitor_frame, text="Нет активных плагинов. Запустите кота, чтобы активировать моды.", fg="grey", bg="#1e1e1e", font=("Arial", 9, "italic")).pack(pady=5)
        else:
            # Выводим список работающих плагинов через запятую или списком
            plugins_text = ", ".join(active_plugins)
            plugins_label = tk.Label(plugins_monitor_frame, text=plugins_text, fg="#ffff00", bg="#1e1e1e", font=("Courier", 10), wraplength=480, justify="left")
            plugins_label.pack(pady=5, padx=5)
        # --------------------------------------

        bottom_frame = tk.Frame(self.root, bg="#1e1e1e")
        bottom_frame.pack(side="bottom", fill="x", pady=10)
        tk.Button(bottom_frame, text="+ СОЗДАТЬ НОВОГО КОТА", font=("Arial", 12, "bold"), bg="#00aa00", fg="white", width=30, height=2, command=self.show_create_menu).pack()

    def confirm_delete(self, cat_name):
        if messagebox.askyesno("Удаление", f"Удалить кота '{cat_name}'?"):
            cat_storage.delete_cat_mod(cat_name)
            self.show_main_menu()

    def show_create_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg="#1e1e1e")
        tk.Label(self.root, text="Название кота:", fg="white", bg="#1e1e1e", font=("Arial", 11, "bold")).pack(pady=5)
        name_entry = tk.Entry(self.root, font=("Arial", 12), width=35, bg="#2d2d2d", fg="white")
        name_entry.pack(pady=5)
        name_entry.insert(0, "Голодный кот")
        
        tk.Label(self.root, text="Кадр 1:", fg="white", bg="#1e1e1e").pack()
        frame1_text = tk.Text(self.root, height=5, width=45, font=("Courier", 12), bg="#2d2d2d", fg="white")
        frame1_text.pack(pady=5)
        frame1_text.insert("1.0", " ( \\_ / ) \n ( ='.'= ) \n ( )_( ) ")
        
        tk.Label(self.root, text="Кадр 2:", fg="white", bg="#1e1e1e").pack()
        frame2_text = tk.Text(self.root, height=5, width=45, font=("Courier", 12), bg="#2d2d2d", fg="white")
        frame2_text.pack(pady=5)
        frame2_text.insert("1.0", " ( \\_ / )   ЖРАТЬ!!!\n ( =^.^= )\n ( )_( ) ")

        def trigger_save():
            success, message = cat_storage.save_cat_mod(name_entry.get().strip(), frame1_text.get("1.0", "end-1c"), frame2_text.get("1.0", "end-1c"))
            if success:
                messagebox.showinfo("Успех", "Кот сохранен в ./mods/cats/")
                self.show_main_menu()
            else:
                messagebox.showerror("Ошибка", message)

        tk.Button(self.root, text="💾 Сохранить кота", bg="#00aa00", fg="white", font=("Arial", 11, "bold"), command=trigger_save).pack(pady=15)
        tk.Button(self.root, text="◀ Отмена", bg="#ff5555", fg="white", font=("Arial", 11), command=self.show_main_menu).pack()

    def start_animation(self, cat_name):
        self.current_frames = self.cats.get(cat_name, cat_storage.DEFAULT_CATS["Ушастый кот"])
        self.current_frame_idx = 0
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg="#000000")
        
        self.label = tk.Label(self.root, text=self.current_frames[self.current_frame_idx], font=("Courier", self.font_size, "bold"), fg=self.get_hex_color(), bg="#000000", justify="left")
        self.label.pack(expand=True, fill="both", pady=10)
        
        control_frame = tk.Frame(self.root, bg="#2d2d2d", bd=2, relief="groove")
        control_frame.pack(fill="x", side="bottom", padx=10, pady=10)
        
        rgb_frame = tk.LabelFrame(control_frame, text="RGB цвет кота", fg="white", bg="#2d2d2d")
        rgb_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="we")
        
        self.r_scale = tk.Scale(rgb_frame, from_=50, to=255, orient="horizontal", bg="#2d2d2d", fg="white", command=self.update_r)
        self.r_scale.set(self.r_val)
        self.r_scale.grid(row=0, column=0, sticky="we", padx=5)
        
        self.g_scale = tk.Scale(rgb_frame, from_=50, to=255, orient="horizontal", bg="#2d2d2d", fg="white", command=self.update_g)
        self.g_scale.set(self.g_val)
        self.g_scale.grid(row=1, column=0, sticky="we", padx=5)
        
        self.b_scale = tk.Scale(rgb_frame, from_=50, to=255, orient="horizontal", bg="#2d2d2d", fg="white", command=self.update_b)
        self.b_scale.set(self.b_val)
        self.b_scale.grid(row=2, column=0, sticky="we", padx=5)
        
        self.disco_btn = tk.Button(rgb_frame, text="🪩 ДИСКОТЕКА: ВЫКЛ", bg="#44aaee", command=self.toggle_disco)
        self.disco_btn.grid(row=3, column=0, pady=5)
        
        tk.Scale(control_frame, from_=10, to=35, orient="horizontal", bg="#2d2d2d", fg="white", label="Размер:", command=self.change_size).grid(row=1, column=0, sticky="we")
        tk.Scale(control_frame, from_=50, to=1000, orient="horizontal", bg="#2d2d2d", fg="white", label="Скорость (мс):", command=self.change_speed).grid(row=2, column=0, sticky="we")
        
        # Панель загрузки стандартных плагинов из нового пути
        plugin_frame = tk.LabelFrame(control_frame, text="Стандартные Моды (./mods/standart/)", fg="yellow", bg="#2d2d2d")
        plugin_frame.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="we")
        
        loaded_plugins = cat_storage.load_plugins(self)
        if not loaded_plugins:
            tk.Label(plugin_frame, text="Поместите .py плагины в ./mods/standart/", fg="grey", bg="#2d2d2d").pack()
        else:
            for plugin in loaded_plugins:
                btn = tk.Button(plugin_frame, text=plugin["button_text"], bg="#444444", fg="white", command=plugin["action"])
                btn.pack(side="left", padx=5, pady=5, fill="x", expand=True)

        tk.Button(control_frame, text="◀ Назад", bg="#ff5555", fg="white", command=self.show_main_menu).grid(row=4, column=0, sticky="we")
        self.animate()

    def update_r(self, val):
        self.r_val = int(val)
        self.update_color()

    def update_g(self, val):
        self.g_val = int(val)
        self.update_color()

    def update_b(self, val):
        self.b_val = int(val)
        self.update_color()

    def update_color(self):
        if hasattr(self, 'label') and self.label.winfo_exists():
            self.label.config(fg=self.get_hex_color())

    def toggle_disco(self):
        self.disco_mode = not self.disco_mode
        if self.disco_mode:
            self.disco_btn.config(text="🪩 ДИСКОТЕКА: ВКЛ", bg="#ff00ff", fg="white")
        else:
            self.disco_btn.config(text="🪩 ДИСКОТЕКА: ВЫКЛ", bg="#44aaee", fg="black")

    def change_size(self, size):
        self.font_size = int(size)
        if hasattr(self, 'label') and self.label.winfo_exists():
            self.label.config(font=("Courier", self.font_size, "bold"))

    def change_speed(self, speed):
        self.anim_speed = int(speed)

    def animate(self):
        if not hasattr(self, 'label') or not self.label.winfo_exists():
            return
        if self.disco_mode:
            self.r_val, self.g_val, self.b_val = random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)
            self.update_color()
        if self.current_frames:
            self.current_frame_idx = (self.current_frame_idx + 1) % len(self.current_frames)
            self.label.config(text=self.current_frames[self.current_frame_idx])
            self.root.after(self.anim_speed, self.animate)