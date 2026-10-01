import tkinter as tk
import os
import sys

from tkinter import ttk

import config
from calc import find_best, get_mark_zones

CANVAS_W, CANVAS_H = 400, 560  
PAD = 12                       
BG = "#f3f3f3"                 


def read_number(entry):
    return float(entry.get().replace(",", "."))

def resource_path(name):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)


def run():
    root = tk.Tk()
    root.title("GridPrint")
    root.resizable(False, False)
    root.configure(bg=BG)
    
    try:
        icon = tk.PhotoImage(file=resource_path("icon-512.png"))
        root.iconphoto(False, icon)
        
    except tk.TclError:
        pass

    # ---------- Стили ----------
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(".", background=BG, font=("Segoe UI", 10))
    style.configure("TLabelframe", background=BG)
    style.configure("TLabelframe.Label", background=BG, font=("Segoe UI", 10, "bold"))
    style.configure("Accent.TButton", font=("Segoe UI", 11, "bold"), padding=8)
    style.configure("Result.TLabel", font=("Segoe UI", 11, "bold"), foreground="#1a5fb4")

    # ---------- Левая часть: форма ----------
    form = ttk.Frame(root)
    form.grid(row=0, column=0, padx=12, pady=12, sticky="n")

    # Рамка «Размеры»
    sizes = ttk.LabelFrame(form, text="Размеры, мм", padding=10)
    sizes.grid(row=0, column=0, sticky="ew")

    def make_entry(parent, row, column, default, width=8):
        entry = ttk.Entry(parent, width=width)
        entry.grid(row=row, column=column, padx=4, pady=4)
        entry.insert(0, default)
        return entry

    ttk.Label(sizes, text="Лист (ширина, высота):").grid(row=0, column=0, sticky="w", pady=4)
    entry_sheet_w = make_entry(sizes, 0, 1, "320")
    entry_sheet_h = make_entry(sizes, 0, 2, "450")

    ttk.Label(sizes, text="Наклейка (ширина, высота):").grid(row=1, column=0, sticky="w", pady=4)
    entry_sticker_w = make_entry(sizes, 1, 1, "50")
    entry_sticker_h = make_entry(sizes, 1, 2, "90")

    ttk.Label(sizes, text="Зазор между наклейками:").grid(row=2, column=0, sticky="w", pady=4)
    entry_gap = make_entry(sizes, 2, 1, "2")

    # Рамка «Параметры»
    options = ttk.LabelFrame(form, text="Параметры", padding=10)
    options.grid(row=1, column=0, sticky="ew", pady=(10, 0))

    marks_var = tk.BooleanVar(value=True)
    ttk.Checkbutton(options, text="Метки включены", variable=marks_var).grid(row=0, column=0, sticky="w")

    # Кнопка и результат
    button = ttk.Button(form, text="Рассчитать", style="Accent.TButton")
    button.grid(row=2, column=0, sticky="ew", pady=(14, 0))

    result_label = ttk.Label(form, text="", style="Result.TLabel", wraplength=300, justify="left")
    result_label.grid(row=3, column=0, sticky="w", pady=(14, 0))

    # ---------- Правая часть: холст ----------
    canvas = tk.Canvas(
        root, width=CANVAS_W, height=CANVAS_H,
        bg="#dcdcdc", highlightthickness=0,
    )
    canvas.grid(row=0, column=1, padx=(0, 12), pady=12)

    # ---------- Рисование ----------
    def draw(layout):
        canvas.delete("all")

        scale = min(
            (CANVAS_W - 2 * PAD) / config.sheet_w,
            (CANVAS_H - 2 * PAD) / config.sheet_h,
        )

        def rect(x1, y1, x2, y2, **kwargs):
            """Рисует прямоугольник, переводя миллиметры в пиксели."""
            canvas.create_rectangle(
                PAD + x1 * scale, PAD + y1 * scale,
                PAD + x2 * scale, PAD + y2 * scale,
                **kwargs,
            )

        # Лист как белая бумага
        rect(0, 0, config.sheet_w, config.sheet_h, fill="white", outline="#888888")

        # Пунктир: граница отступа margin от края листа
        rect(
            config.margin, config.margin,
            config.sheet_w - config.margin, config.sheet_h - config.margin,
            outline="#aaaaaa", dash=(3, 3),
        )

        # Зоны меток (считаем заново при каждой отрисовке)
        zones = get_mark_zones(
            config.BOTTOM_RIGHT_MARK, config.BOTTOM_LEFT_MARK,
            config.TOP_RIGHT_MARK, config.TOP_LEFT_MARK,
        )
        for x1, y1, x2, y2 in zones:
            rect(x1, y1, x2, y2, fill="#e53935", outline="")

        # Наклейки
        for x1, y1, x2, y2 in layout:
            rect(x1, y1, x2, y2, fill="#d6e6ff", outline="#1a5fb4")

    # ---------- Кнопка ----------
    def on_click():
        try:
            sheet_w = read_number(entry_sheet_w)
            sheet_h = read_number(entry_sheet_h)
            sticker_w = read_number(entry_sticker_w)
            sticker_h = read_number(entry_sticker_h)
            gap = read_number(entry_gap)
        except ValueError:
            result_label.config(text="Введите числа")
            return

        if min(sheet_w, sheet_h, sticker_w, sticker_h) < 1 or gap < 0:
            result_label.config(text="Размеры должны быть больше нуля")
            return

        config.sheet_w = sheet_w
        config.sheet_h = sheet_h
        config.sticker_w = sticker_w
        config.sticker_h = sticker_h
        config.gap = gap
        config.marks_on = marks_var.get()

        layout, w, h, c, r = find_best()

        if not layout:
            canvas.delete("all")
            result_label.config(text="Наклейки не помещаются")
            return

        draw(layout)

        used = len(layout) * w * h / (sheet_w * sheet_h) * 100
        rotated = "\nНаклейки повёрнуты" if w != sticker_w else ""
        result_label.config(
            text=f"Наклеек: {len(layout)} ({c} x {r})\nИспользовано листа: {used:.1f}%{rotated}"
        )

    button.config(command=on_click)

    # ---------- Окно по центру экрана ----------
    root.update_idletasks()  
    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) // 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) // 2 - 20
    root.geometry(f"+{x}+{y}")

    root.mainloop()