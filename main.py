import json
import math
import os
import flet as ft

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "formulas.json")

SUBJECT_COLORS = {
    "Физика": ft.Colors.CYAN_400,
    "Математика": ft.Colors.AMBER_400,
    "Химия": ft.Colors.PURPLE_400,
    "Информатика": ft.Colors.GREEN_400,
}

SAFE_MATH = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "pi": math.pi,
    "e": math.e,
    "log": math.log,
    "log2": math.log2,
    "log10": math.log10,
    "abs": abs,
    "round": round,
    "pow": pow,
}

def load_data():
    if not os.path.exists(JSON_PATH):
        return {}
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)
            if isinstance(raw, list):
                grouped = {}
                for item in raw:
                    subj = str(item.get("subject", "Физика")).strip()
                    grouped.setdefault(subj, []).append(item)
                return grouped
            elif isinstance(raw, dict):
                return raw
    except Exception:
        pass
    return {}

def calculate_expression(expr: str, var_values: dict):
    clean_expr = expr.replace("^", "**")
    context = dict(SAFE_MATH)
    context.update(var_values)
    return eval(clean_expr, {"__builtins__": {}}, context)

def build_calculator_ui(formula_item: dict, accent_color):
    var_defs = formula_item.get("vars", [])
    expr = formula_item.get("expression")
    unit = formula_item.get("unit", "")

    if not var_defs or not expr:
        return ft.Container()

    inputs = {}
    result_text = ft.Text("Введите значения параметров", size=13, color=ft.Colors.GREY_400, selectable=True)

    input_fields = []
    for var in var_defs:
        sym = var.get("symbol", "")
        lbl = var.get("label", sym)
        tf = ft.TextField(
            label=lbl,
            keyboard_type=ft.KeyboardType.NUMBER,
            dense=True,
            expand=True,
        )
        inputs[sym] = tf
        input_fields.append(ft.Container(content=tf, width=160))

    def on_calc_click(e):
        try:
            parsed_vals = {}
            for sym, field in inputs.items():
                val_str = (field.value or "").strip().replace(",", ".")
                if not val_str:
                    result_text.value = f"Заполните: {field.label}"
                    result_text.color = ft.Colors.RED_300
                    e.page.update()
                    return
                parsed_vals[sym] = float(val_str)

            res = calculate_expression(expr, parsed_vals)
            formatted = f"{res:.4g}" if isinstance(res, (int, float)) else str(res)
            result_text.value = f"Результат: {formatted} {unit}".strip()
            result_text.color = accent_color
        except ZeroDivisionError:
            result_text.value = "Ошибка: деление на ноль"
            result_text.color = ft.Colors.RED_300
        except Exception:
            result_text.value = "Ошибка вычисления"
            result_text.color = ft.Colors.RED_300
        e.page.update()

    calc_body = ft.Column([
        ft.Text("Калькулятор формулы", weight=ft.FontWeight.BOLD, size=14, color=accent_color),
        ft.Row(input_fields, wrap=True, spacing=10),
        ft.Row([
            ft.Container(
                content=ft.Text("Рассчитать", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=13),
                padding=10,
                bgcolor=ft.Colors.BLUE_700,
                border_radius=8,
                on_click=on_calc_click,
            ),
            ft.Container(content=result_text, expand=True),
        ], wrap=True, spacing=10, alignment=ft.MainAxisAlignment.START),
    ], spacing=10, visible=False)

    def toggle_calc(e):
        calc_body.visible = not calc_body.visible
        toggle_btn.content.value = "Скрыть калькулятор" if calc_body.visible else "Открыть калькулятор"
        e.page.update()

    toggle_btn = ft.Container(
        content=ft.Text("Открыть калькулятор", size=13, color=accent_color, weight=ft.FontWeight.W_600),
        padding=6,
        on_click=toggle_calc,
    )

    return ft.Container(
        content=ft.Column([toggle_btn, calc_body], spacing=6),
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
        padding=10,
        border_radius=8,
    )

def main(page: ft.Page):
    page.title = "Справочник формул"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 12
    page.scroll = ft.ScrollMode.AUTO

    data = load_data()
    subjects = list(data.keys()) if data else ["Физика", "Математика", "Химия", "Информатика"]
    current_subject = [subjects[0] if subjects else "Физика"]

    cards_column = ft.Column(spacing=12, expand=True)

    def update_view():
        cards_column.controls.clear()
        subj = current_subject[0]
        items = data.get(subj, [])
        query = (search_field.value or "").strip().lower()

        filtered = [
            x for x in items
            if query in str(x.get("title") or x.get("name") or "").lower()
            or query in str(x.get("formula", "")).lower()
            or query in str(x.get("description", "")).lower()
            or query in str(x.get("topic", "")).lower()
        ]

        if not filtered:
            cards_column.controls.append(
                ft.Text("Формулы не найдены", size=15, color=ft.Colors.GREY_400)
            )
        else:
            accent = SUBJECT_COLORS.get(subj, ft.Colors.BLUE_400)
            for f in filtered:
                t_title = f.get("title") or f.get("name") or "Формула"
                t_topic = f.get("topic", subj)

                card_elements = [
                    ft.Row([
                        ft.Text(
                            str(t_title),
                            size=17,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE,
                            expand=True,
                            no_wrap=False,
                        ),
                        ft.Container(
                            content=ft.Text(str(t_topic), size=11, color=accent),
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
                            padding=6,
                            border_radius=6,
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.START),
                    ft.Text(
                        str(f.get("formula", "")),
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=accent,
                        selectable=True,
                        no_wrap=False,
                    ),
                    ft.Text(
                        str(f.get("description", "")),
                        size=13,
                        color=ft.Colors.GREY_300,
                        no_wrap=False,
                    ),
                ]

                calc_widget = build_calculator_ui(f, accent)
                if calc_widget.content:
                    card_elements.append(calc_widget)

                if f.get("task"):
                    card_elements.append(
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Пример задачи:", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_400),
                                ft.Text(str(f.get("task")), size=13, color=ft.Colors.GREY_300, no_wrap=False),
                                ft.Text(f"Решение: {f.get('solution', '')}", size=13, color=accent, no_wrap=False),
                            ], spacing=4),
                            padding=10,
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
                            border_radius=8,
                        )
                    )

                cards_column.controls.append(
                    ft.Container(
                        content=ft.Column(card_elements, spacing=8),
                        padding=12,
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                        border_radius=10,
                    )
                )
        page.update()

    def select_subj(e):
        current_subject[0] = e.control.data
        for c in nav_row.controls:
            c.bgcolor = ft.Colors.BLUE_700 if c.data == current_subject[0] else ft.Colors.SURFACE_CONTAINER_HIGH
        update_view()

    search_field = ft.TextField(
        hint_text="Поиск формулы или темы...",
        prefix_icon=ft.Icons.SEARCH,
        on_change=lambda e: update_view(),
        expand=True,
        dense=True,
    )

    nav_row = ft.Row(spacing=8, wrap=True)
    for s in subjects:
        nav_row.controls.append(
            ft.Container(
                content=ft.Text(s, color=ft.Colors.WHITE, size=13),
                data=s,
                padding=8,
                bgcolor=ft.Colors.BLUE_700 if s == current_subject[0] else ft.Colors.SURFACE_CONTAINER_HIGH,
                border_radius=8,
                on_click=select_subj,
            )
        )

    page.add(
        ft.Text("Справочник формул", size=22, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        ft.Row([search_field]),
        nav_row,
        ft.Container(height=6),
        cards_column,
    )
    update_view()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8555))
    ft.run(main, host="0.0.0.0", port=port)