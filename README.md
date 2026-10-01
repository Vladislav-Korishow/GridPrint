# GridPrint

**English** | [Русский](#русская-версия)

A desktop tool for print shops: it calculates how many stickers fit on a large printing sheet and shows the layout.

It takes into account corner registration marks (each corner can have its own size), the gap between stickers, and the margin from the sheet edges. The program picks the best layout on its own: it tries rotating the sticker by 90° and changing the number of columns and rows to fit as many stickers as possible.

## Features

- Sheet and sticker sizes in millimeters
- Adjustable gap between stickers
- Registration marks can be switched on and off with one checkbox
- Corner marks of different sizes (set in `config.py`)
- Margin from the sheet edge and from the marks
- Automatic search over variants: sticker rotation, number of columns and rows
- The grid is centered on the sheet
- Layout preview in the window: sheet, forbidden mark zones, stickers, margin boundary
- Result: sticker count, grid (columns × rows), rotation, sheet usage in percent
- Accepts decimal numbers; a comma instead of a dot works too


## How it works

1. The sheet and stickers are described as rectangles `(x1, y1, x2, y2)`. The origin is the top-left corner, the Y axis points down.
2. A forbidden zone is built around each mark: the mark size plus the `margin`.
3. For a sticker, the program counts how many fit in a row and in a column:
   `n = floor((free_length + gap) / (size + gap))`
4. The grid is centered on the sheet, then every sticker that intersects a forbidden zone is removed.
5. Steps 3–4 are repeated for 8 variants (sticker as is or rotated, maximum number of columns or one less, maximum number of rows or one less). The variant with the most stickers wins.

## Installation and running

Requires **Python 3.10 or newer**. No external libraries are needed: `tkinter` ships with Python.

```bash
git clone https://github.com/Vladislav-Korishow/GridPrint.git
cd GridPrint
python main.py
```

## Configuration

Mark sizes and the margin are set in `config.py`:

```python
BOTTOM_RIGHT_MARK = 16.0, 18.5   # (width, height) of the mark, mm
BOTTOM_LEFT_MARK = 16.0, 16.0
TOP_RIGHT_MARK = 16.0, 16.0
TOP_LEFT_MARK = 16.0, 16.0

margin = 6                       # margin from the sheet edge and from the marks, mm
```

All other values (sheet, sticker, gap, marks on/off) are entered in the program window. The values in `config.py` for them only serve as initial defaults.

## Building an exe (Windows)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon-512.png --add-data "icon-512.png;." main.py
```

The result appears in the `dist` folder. The window icon is packed inside the exe, so nothing needs to be placed next to it. After editing `config.py`, rebuild the exe.

## Project structure

```
main.py       entry point, starts the window
gui.py        tkinter interface: input fields, button, layout canvas
calc.py       calculations: mark zones, grid, intersections, best-variant search
config.py     constants: mark sizes, margin, default values
icon-512.png  window icon
my_icon.ico   exe file icon
```

`calc.py` does not depend on the interface, so the calculation can be used and run separately.

## Limitations

- The layout is always a single even grid centered on the sheet. Stickers of different orientations are not mixed in one layout.
- Marks are treated as rectangles in the corners. The complex shape of the red line around the marks is not modeled; a forbidden zone with a margin is used instead.
- All sizes are in millimeters.

## License

Choose a license (for example, MIT) and add a `LICENSE` file.

---

# Русская версия

[English](#gridprint) | **Русский**

Программа для полиграфии: считает, сколько наклеек помещается на большом печатном листе, и показывает схему раскладки.

Учитывает метки в углах листа (у каждого угла свой размер), зазор между наклейками и отступ от краёв. Сама подбирает лучший вариант: пробует повернуть наклейку на 90° и менять число столбцов и рядов, чтобы получить максимум наклеек.

## Возможности

- Ввод размеров листа и наклейки в миллиметрах
- Настраиваемый зазор между наклейками
- Включение и выключение меток одной галочкой
- Метки в углах разного размера (задаются в `config.py`)
- Отступ от края листа и от меток
- Автоматический перебор вариантов: поворот наклейки, число столбцов и рядов
- Сетка располагается по центру листа
- Схема раскладки в окне: лист, запретные зоны меток, наклейки, граница отступа
- Результат: количество наклеек, сетка (столбцы × ряды), поворот, процент использования листа
- Принимает дробные числа, запятая вместо точки тоже работает


## Как это работает

1. Лист и наклейки описываются прямоугольниками `(x1, y1, x2, y2)`, начало координат в левом верхнем углу, ось Y направлена вниз.
2. Вокруг каждой метки строится запретная зона: размер метки плюс отступ `margin`.
3. Для наклейки считается, сколько штук помещается в ряд и в столбец:
   `n = floor((свободная_длина + зазор) / (размер + зазор))`
4. Сетка ставится по центру листа, затем из неё убираются наклейки, которые пересекаются с запретными зонами.
5. Шаги 3–4 повторяются для 8 вариантов (наклейка как есть или повёрнутая, столбцов максимум или на один меньше, рядов максимум или на один меньше). Побеждает вариант с наибольшим числом наклеек.

## Установка и запуск

Требуется **Python 3.10 или новее**. Внешние библиотеки не нужны: `tkinter` входит в стандартную поставку Python.

```bash
git clone https://github.com/Vladislav-Korishow/GridPrint.git
cd GridPrint
python main.py
```

## Настройка

Размеры меток и отступ задаются в файле `config.py`:

```python
BOTTOM_RIGHT_MARK = 16.0, 18.5   # (ширина, высота) метки, мм
BOTTOM_LEFT_MARK = 16.0, 16.0
TOP_RIGHT_MARK = 16.0, 16.0
TOP_LEFT_MARK = 16.0, 16.0

margin = 6                       # отступ от края листа и от меток, мм
```

Остальные значения (лист, наклейка, зазор, метки вкл/выкл) вводятся в окне программы. Значения в `config.py` для них служат только начальными.

## Сборка в exe (Windows)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon-512.png --add-data "icon-512.png;." main.py
```

Готовый файл появится в папке `dist`. Иконка окна упакована внутрь exe, рядом с ним ничего класть не нужно. После изменения `config.py` exe нужно собрать заново.

## Структура проекта

```
main.py       точка входа, запускает окно
gui.py        интерфейс на tkinter: поля ввода, кнопка, схема на холсте
calc.py       расчёты: зоны меток, сетка, пересечения, поиск лучшего варианта
config.py     константы: размеры меток, отступ, начальные значения
icon-512.png  иконка окна
my_icon.ico   иконка exe-файла
```

`calc.py` не зависит от интерфейса, поэтому расчёт можно использовать и запускать отдельно.

## Ограничения

- Раскладка всегда одна ровная сетка по центру листа. Наклейки разных ориентаций в одной раскладке не смешиваются.
- Метки считаются прямоугольниками в углах листа. Сложная форма красной линии вокруг меток не моделируется, вместо неё используется запретная зона с отступом.
- Все размеры в миллиметрах.

