import config

def get_mark_zones(
    bottom_right: tuple[int | float],
    bottom_left: tuple[int | float],
    top_right: tuple[int | float],
    top_left: tuple[int | float],
) -> list[tuple]:
    """Получает размеры четырёх меток и вычисляет по ним координаты четырёх запрещённых зон."""

    if config.marks_on == False:
        return []
    
    mark_zones = []
    mark_w, mark_h = bottom_right
    mark_zones.append(
        (config.sheet_w - (mark_w + config.margin), config.sheet_h - (mark_h + config.margin), config.sheet_w, config.sheet_h)
    )
    mark_w, mark_h = bottom_left
    mark_zones.append((0, config.sheet_h - (mark_h + config.margin), mark_w + config.margin, config.sheet_h))
    mark_w, mark_h = top_right
    mark_zones.append((config.sheet_w - (mark_w + config.margin), 0, config.sheet_w, mark_h + config.margin))
    mark_w, mark_h = top_left
    mark_zones.append((0, 0, mark_w + config.margin, mark_h + config.margin))
    return mark_zones


def calc_grid(
    sheet_w: int | float,
    sheet_h: int | float,
    sticker_w: int | float,
    sticker_h: int | float,
) -> tuple[int]:
    """Считает сколько наклеек помещается по ширине и высоте"""
    cols = int(
        ((sheet_w - (config.margin * 2)) + config.gap) / (sticker_w + config.gap)
    )  # Количество наклеек по ширине (столбцы)
    rows = int(
        ((sheet_h - (config.margin * 2)) + config.gap) / (sticker_h + config.gap)
    )  # Количество наклеект по высоте (ряды)
    return cols, rows


def intersects(a: tuple[int | float], b: tuple[int | float]) -> bool:
    """Проверяет, пересекаются ли два прямоугольника"""

    a_x1, a_y1, a_x2, a_y2 = a  # Координаты наклейки
    b_x1, b_y1, b_x2, b_y2 = b  # Координаты запрещённой зоны
    return not (a_x2 <= b_x1 or a_x1 >= b_x2 or a_y2 <= b_y1 or a_y1 >= b_y2)


def build_layout(
    sticker_w: int | float, sticker_h: int | float, cols: int | float, rows: int | float
) -> list[tuple]:
    """Выстраиваем макет сетки"""

    mark_zones = get_mark_zones(
        config.BOTTOM_RIGHT_MARK, config.BOTTOM_LEFT_MARK, config.TOP_RIGHT_MARK, config.TOP_LEFT_MARK
    )  # Получаем координаты запрещённых зон

    grid_w = cols * sticker_w + (cols - 1) * config.gap  # Общая ширина всей сетки
    grid_h = rows * sticker_h + (rows - 1) * config.gap  # Общая высота всей сетки
    x0 = (config.sheet_w - grid_w) / 2  # Начальная координата X всей группы наклеек
    y0 = (config.sheet_h - grid_h) / 2  # Начальная координата Y всей группы наклеек

    """Вычисляем координаты каждой наклейки и записываем в список"""
    stickers = []
    for row in range(rows):
        for col in range(cols):
            x1 = x0 + col * (sticker_w + config.gap)  # левый верхний угол
            y1 = y0 + row * (sticker_h + config.gap)  # левый нижний угол
            x2 = x1 + sticker_w  # правый верхний угол
            y2 = y1 + sticker_h  # правый нижний угол
            stickers.append((x1, y1, x2, y2))

    """Формируем список наклеек, которые не пересекаются ни с одной запрещённой зоной"""
    good_stickers = []
    for sticker in stickers:
        ok = True
        for zone in mark_zones:
            if intersects(sticker, zone):
                ok = False
        if ok:
            good_stickers.append(sticker)

    return good_stickers


def find_best() -> tuple[list | tuple]:
    """Перебирает варианты ориентации и размера сетки и выбирает вариант с максимальным количеством наклеек"""
    best_layout = []
    best_w, best_h = 0, 0
    best_c, best_r = 0, 0

    for w, h in [(config.sticker_w, config.sticker_h), (config.sticker_h, config.sticker_w)]:
        cols, rows = calc_grid(config.sheet_w, config.sheet_h, w, h)
        for c in [cols, cols - 1]:
            for r in [rows, rows - 1]:
                if c < 1 or r < 1:
                    continue
                layout = build_layout(w, h, c, r)
                if len(layout) > len(best_layout):
                    best_layout = layout
                    best_w, best_h = w, h
                    best_c, best_r = c, r

    return best_layout, best_w, best_h, best_c, best_r

print(find_best())