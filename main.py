import json
import math
import os
import flet as ft

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "formulas.json")

def load_formulas():
    if os.path.exists(JSON_PATH):
        try:
            with open(JSON_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data:
                    return data
        except Exception as ex:
            print("Ошибка загрузки formulas.json:", ex)
    return []

formulas_db = load_formulas()

def main(page: ft.Page):
    page.title = "Интерактивный справочник формул"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 15
    page.spacing = 15
    page.scroll = ft.ScrollMode.AUTO

    current_subject = "Все"
    search_query = ""

    cards_column = ft.Column(spacing=12)

    def calculate_result(formula_id, inputs_dict, result_text):
        try:
            # --- ФИЗИКА ---
            if formula_id == "speed":
                s = float(inputs_dict["s"].value)
                t = float(inputs_dict["t"].value)
                if t == 0:
                    result_text.value = "Ошибка: время не может быть 0"
                    result_text.color = ft.Colors.RED_400
                else:
                    v = s / t
                    result_text.value = f"Ответ: v = {v:.2f} м/с ({v * 3.6:.2f} км/ч)"
                    result_text.color = ft.Colors.GREEN_400

            elif formula_id == "acceleration":
                v = float(inputs_dict["v"].value)
                v0 = float(inputs_dict["v0"].value)
                t = float(inputs_dict["t"].value)
                if t == 0:
                    result_text.value = "Ошибка: время не может быть 0"
                    result_text.color = ft.Colors.RED_400
                else:
                    result_text.value = f"Ответ: a = {(v - v0) / t:.2f} м/с²"
                    result_text.color = ft.Colors.GREEN_400

            elif formula_id == "displacement":
                v0 = float(inputs_dict["v0"].value)
                a = float(inputs_dict["a"].value)
                t = float(inputs_dict["t"].value)
                result_text.value = f"Ответ: s = {v0 * t + (a * (t ** 2)) / 2:.2f} м"
                result_text.color = ft.Colors.GREEN_400

            elif formula_id == "force":
                m = float(inputs_dict["m"].value)
                a = float(inputs_dict["a"].value)
                result_text.value = f"Ответ: F = {m * a:.2f} Н"
                result_text.color = ft.Colors.GREEN_400

            elif formula_id == "density":
                m = float(inputs_dict["m"].value)
                v_vol = float(inputs_dict["v"].value)
                if v_vol == 0:
                    result_text.value = "Ошибка: объём не может быть 0"
                    result_text.color = ft.Colors.RED_400
                else:
                    result_text.value = f"Ответ: ρ = {m / v_vol:.2f} кг/м³"
                    result_text.color = ft.Colors.GREEN_400

            elif formula_id == "gravity_force":
                m = float(inputs_dict["m"].value)
                g = float(inputs_dict["g"].value) if inputs_dict["g"].value else 9.8
                result_text.value = f"Ответ: F_тяж = {m * g:.2f} Н"
                result_text.color = ft.Colors.GREEN_400

            elif formula_id == "hooke_law":
                k = float(inputs_dict["k"].value)
                x = float(inputs_dict["x"].value)
                result_text.value = f"Ответ: F_упр = {k * x:.2f} Н"
                result_text.color = ft.Colors.GREEN_400

            elif formula_id == "friction_force":
                mu = float(inputs_dict["mu"].value)
                n = float(inputs_dict["n"].value)
                result_text.value = f"Ответ: F_тр = {mu * n:.2f} Н"
                result_text.color = ft.Colors.GREEN_400

            elif formula_id == "pressure":
                f_val = float(inputs_dict["f"].value)
                s_val = float(inputs_dict["s"].value)
                if s_val == 0:
                    result_text.value = "Ошибка: площадь не может быть 0"
                    result_text.color = ft.Colors.RED_400
                else:
                    result_text.value = f"Ответ: P = {f_val / s_val:.2f} Па"
                    result_text.color = ft.Colors.GREEN_400

            elif formula_id == "hydrostatic_p":
                rho = float(inputs_dict["rho"].value)
                h = float(inputs_dict["h"].value)
                g = float(inputs_dict["g"].value) if inputs_dict["g"].value else 9.8
                p = rho * g * h
                result_text.value = f"Ответ: P = {p:.2f} Па ({p / 1000:.2f} кПа)"
                result_text.color = ft.Colors.GREEN_400

            elif formula_id == "archimedes":
                rho = float(inputs_dict["rho"].value)
                v = float(inputs_dict["v"].value)
                g = float(inputs_dict["g"].value) if inputs_dict["g"].value else 9.8
                result_text.value = f"Ответ: F_а = {rho * g * v:.2f} Н"
                result_text.color = ft.Colors.GREEN_400

            elif formula_id == "work":
                f_val = float(inputs_dict["f"].value)
                s_val = float(inputs_dict["s"].value)
                result_text.value = f"Ответ: A = {f_val * s_val:.2f} Дж"
                result_text.color = ft.Colors.GREEN_400

            elif formula_id == "power":
                a_val = float(inputs_dict["a"].value)
                t_val = float(inputs_dict["t"].value)
                if t_val == 0:
                    result_text.value = "Ошибка: время не может быть 0"
                    result_text.color = ft.Colors.RED_400
                else:
                    result_text.value = f"Ответ: N = {a_val / t_val:.2f} Вт"
                    result_text.color = ft.Colors.GREEN_400

            elif formula_id == "kinetic_energy":
                m = float(inputs_dict["m"].value)
                v = float(inputs_dict["v"].value)
                result_text.value = f"Ответ: E_k = {(m * (v ** 2)) / 2:.2f} Дж"
                result_text.color = ft.Colors.GREEN_400

            elif formula_id == "potential_energy":
                m = float(inputs_dict["m"].value)
                h = float(inputs_dict["h"].value)
                g = float(inputs_dict["g"].value) if inputs_dict["g"].value else 9.8
                result_text.value = f"Ответ: E_p = {m * g * h:.2f} Дж"
                result_text.color = ft.Colors.GREEN_400

            elif formula_id == "ohm":
                u = float(inputs_dict["u"].value)
                r = float(inputs_dict["r"].value)
                if r == 0:
                    result_text.value = "Ошибка: сопротивление не может быть 0"
                    result_text.color = ft.Colors.RED_400
                else:
                    result_text.value = f"Ответ: I = {u / r:.2f} А"
                    result_text.color = ft.Colors.GREEN_400

            elif formula_id == "joule_lenz":
                i = float(inputs_dict["i"].value)
                r = float(inputs_dict["r"].value)
                t = float(inputs_dict["t"].value)
                result_text.value = f"Ответ: Q = {(i ** 2) * r * t:.2f} Дж"
                result_text.color = ft.Colors.GREEN_400

            # --- МАТЕМАТИКА ---
            elif formula_id == "pythagoras":
                a = float(inputs_dict["a"].value)
                b = float(inputs_dict["b"].value)
                result_text.value = f"Ответ: c = {math.sqrt(a**2 + b**2):.2f}"
                result_text.color = ft.Colors.GREEN_400

            elif formula_id == "quadratic":
                a = float(inputs_dict["a"].value)
                b = float(inputs_dict["b"].value)
                c = float(inputs_dict["c"].value)
                d = b**2 - 4 * a * c
                if d < 0:
                    result_text.value = f"D = {d:.2f} (действительных корней нет)"
                    result_text.color = ft.Colors.AMBER_400
                elif d == 0:
                    result_text.value = f"D = 0, один корень: x = {-b / (2 * a):.2f}"
                    result_text.color = ft.Colors.GREEN_400
                else:
                    x1 = (-b + math.sqrt(d)) / (2 * a)
                    x2 = (-b - math.sqrt(d)) / (2 * a)
                    result_text.value = f"D = {d:.2f} => x₁ = {x1:.2f}, x₂ = {x2:.2f}"
                    result_text.color = ft.Colors.GREEN_400

            elif formula_id == "triangle_area":
                a = float(inputs_dict["a"].value)
                h = float(inputs_dict["h"].value)
                result_text.value = f"Ответ: S = {(a * h) / 2:.2f}"
                result_text.color = ft.Colors.GREEN_400

            elif formula_id == "circle_area":
                r = float(inputs_dict["r"].value)
                result_text.value = f"Ответ: S = {math.pi * (r ** 2):.2f}"
                result_text.color = ft.Colors.GREEN_400

            elif formula_id == "trapezoid_area":
                a = float(inputs_dict["a"].value)
                b = float(inputs_dict["b"].value)
                h = float(inputs_dict["h"].value)
                result_text.value = f"Ответ: S = {((a + b) / 2) * h:.2f}"
                result_text.color = ft.Colors.GREEN_400

            elif formula_id == "cylinder_vol":
                r = float(inputs_dict["r"].value)
                h = float(inputs_dict["h"].value)
                result_text.value = f"Ответ: V = {math.pi * (r ** 2) * h:.2f}"
                result_text.color = ft.Colors.GREEN_400

            elif formula_id == "sphere_vol":
                r = float(inputs_dict["r"].value)
                result_text.value = f"Ответ: V = {(4 / 3) * math.pi * (r ** 3):.2f}"
                result_text.color = ft.Colors.GREEN_400

            elif formula_id == "arithmetic_prog":
                a1 = float(inputs_dict["a1"].value)
                d = float(inputs_dict["d"].value)
                n = float(inputs_dict["n"].value)
                result_text.value = f"Ответ: a_{int(n)} = {a1 + d * (n - 1):.2f}"
                result_text.color = ft.Colors.GREEN_400

            elif formula_id == "geom_prog":
                b1 = float(inputs_dict["b1"].value)
                q = float(inputs_dict["q"].value)
                n = float(inputs_dict["n"].value)
                result_text.value = f"Ответ: b_{int(n)} = {b1 * (q ** (n - 1)):.2f}"
                result_text.color = ft.Colors.GREEN_400

            # --- ХИМИЯ ---
            elif formula_id == "mass_fraction":
                m_solute = float(inputs_dict["m_solute"].value)
                m_solution = float(inputs_dict["m_solution"].value)
                if m_solution == 0:
                    result_text.value = "Ошибка: масса раствора не может быть 0"
                    result_text.color = ft.Colors.RED_400
                else:
                    result_text.value = f"Ответ: ω = {(m_solute / m_solution) * 100:.2f}%"
                    result_text.color = ft.Colors.GREEN_400

            elif formula_id == "amount_substance":
                m = float(inputs_dict["m"].value)
                m_molar = float(inputs_dict["m_molar"].value)
                if m_molar == 0:
                    result_text.value = "Ошибка: молярная масса не может быть 0"
                    result_text.color = ft.Colors.RED_400
                else:
                    result_text.value = f"Ответ: n = {m / m_molar:.2f} моль"
                    result_text.color = ft.Colors.GREEN_400

            elif formula_id == "gas_volume":
                n = float(inputs_dict["n"].value)
                result_text.value = f"Ответ: V = {n * 22.4:.2f} л (при н.у.)"
                result_text.color = ft.Colors.GREEN_400

            elif formula_id == "avogadro_number":
                n = float(inputs_dict["n"].value)
                particles = n * 6.022e23
                result_text.value = f"Ответ: N = {particles:.3e} молекул"
                result_text.color = ft.Colors.GREEN_400

            elif formula_id == "molar_conc":
                n = float(inputs_dict["n"].value)
                v = float(inputs_dict["v"].value)
                if v == 0:
                    result_text.value = "Ошибка: объём не может быть 0"
                    result_text.color = ft.Colors.RED_400
                else:
                    result_text.value = f"Ответ: C = {n / v:.2f} моль/л (М)"
                    result_text.color = ft.Colors.GREEN_400

            # --- ИНФОРМАТИКА ---
            elif formula_id == "info_vol":
                k = float(inputs_dict["k"].value)
                i_bit = float(inputs_dict["i"].value)
                bits = k * i_bit
                bytes_val = bits / 8
                kbytes_val = bytes_val / 1024
                result_text.value = f"Ответ: {bits:.0f} бит ({bytes_val:.1f} байт / {kbytes_val:.2f} Кбайт)"
                result_text.color = ft.Colors.GREEN_400

            elif formula_id == "hartley":
                n = float(inputs_dict["n"].value)
                if n <= 0:
                    result_text.value = "Ошибка: N должно быть > 0"
                    result_text.color = ft.Colors.RED_400
                else:
                    i_val = math.log2(n)
                    result_text.value = f"Ответ: i = log₂(N) = {i_val:.2f} бит (округленно: {math.ceil(i_val)} бит)"
                    result_text.color = ft.Colors.GREEN_400

            elif formula_id == "image_vol":
                x = float(inputs_dict["x"].value)
                y = float(inputs_dict["y"].value)
                i_depth = float(inputs_dict["i"].value)
                bits = x * y * i_depth
                kbytes = bits / (8 * 1024)
                mbytes = kbytes / 1024
                result_text.value = f"Ответ: {kbytes:.1f} Кбайт ({mbytes:.2f} Мбайт)"
                result_text.color = ft.Colors.GREEN_400

            elif formula_id == "audio_transfer":
                f_freq = float(inputs_dict["f"].value)
                i_res = float(inputs_dict["i"].value)
                t_sec = float(inputs_dict["t"].value)
                k_chan = float(inputs_dict["k"].value)
                bits = f_freq * i_res * t_sec * k_chan
                mbytes = bits / (8 * 1024 * 1024)
                result_text.value = f"Ответ: {bits:.0f} бит ({mbytes:.2f} Мбайт)"
                result_text.color = ft.Colors.GREEN_400

            elif formula_id == "transfer_speed":
                v_speed = float(inputs_dict["v"].value)
                t_sec = float(inputs_dict["t"].value)
                kbits = v_speed * t_sec
                kbytes = kbits / 8
                result_text.value = f"Ответ: Q = {kbits:.1f} Кбит ({kbytes:.1f} Кбайт / {kbytes / 1024:.2f} Мбайт)"
                result_text.color = ft.Colors.GREEN_400

            else:
                result_text.value = "Калькулятор для этой формулы в разработке"
                result_text.color = ft.Colors.AMBER_400

        except ValueError:
            result_text.value = "Ошибка: заполните поля числами"
            result_text.color = ft.Colors.RED_400
        page.update()

    def build_card(formula):
        calc_inputs = {}
        calc_fields_row = ft.Row(wrap=True, spacing=10)
        result_text = ft.Text("", size=14, weight=ft.FontWeight.W_600)

        fields = formula.get("calc_fields", [])
        for field in fields:
            tf = ft.TextField(
                label=field.get("label", field["name"]),
                width=175,
                height=45,
                text_size=13,
                content_padding=10,
                keyboard_type=ft.KeyboardType.NUMBER
            )
            calc_inputs[field["name"]] = tf
            calc_fields_row.controls.append(tf)

        calc_box = ft.Column(
            visible=False,
            spacing=10,
            controls=[
                calc_fields_row,
                ft.FilledButton(
                    "Рассчитать",
                    on_click=lambda _: calculate_result(formula.get("id"), calc_inputs, result_text)
                ),
                result_text
            ]
        )

        task_text = formula.get("example_task", "Пример задачи скоро появится.")
        task_box = ft.Container(
            visible=False,
            content=ft.Column(
                spacing=5,
                controls=[
                    ft.Text("Условие и разбор задачи:", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_200),
                    ft.Text(task_text, size=13, color=ft.Colors.GREY_200)
                ]
            ),
            bgcolor=ft.Colors.GREY_800,
            padding=10,
            border_radius=8
        )

        def toggle_calc(e):
            calc_box.visible = not calc_box.visible
            toggle_calc_btn.text = "Скрыть калькулятор" if calc_box.visible else "Калькулятор"
            page.update()

        def toggle_task(e):
            task_box.visible = not task_box.visible
            toggle_task_btn.text = "Скрыть задачу" if task_box.visible else "Пример задачи"
            page.update()

        toggle_calc_btn = ft.OutlinedButton("Калькулятор", on_click=toggle_calc)
        toggle_task_btn = ft.OutlinedButton("Пример задачи", on_click=toggle_task)

        return ft.Container(
            content=ft.Column(
                spacing=10,
                tight=True,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(formula.get("title", ""), size=17, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            ft.Container(
                                content=ft.Text(formula.get("subject", ""), size=11, color=ft.Colors.BLUE_200),
                                bgcolor=ft.Colors.BLUE_900,
                                padding=8,
                                border_radius=6
                            )
                        ]
                    ),
                    ft.Text(formula.get("formula", ""), size=19, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_300),
                    ft.Text(formula.get("description", ""), size=13, color=ft.Colors.GREY_300),
                    ft.Row(spacing=10, controls=[toggle_task_btn, toggle_calc_btn]),
                    task_box,
                    calc_box
                ]
            ),
            bgcolor=ft.Colors.GREY_900,
            border_radius=12,
            padding=16,
            border=ft.Border.all(width=1, color=ft.Colors.GREY_800)
        )

    def update_cards():
        cards_column.controls.clear()
        for f in formulas_db:
            subj_match = current_subject == "Все" or f.get("subject", "").strip().lower() == current_subject.strip().lower()
            query_match = (
                search_query.lower() in f.get("title", "").lower() or
                search_query.lower() in f.get("formula", "").lower() or
                search_query.lower() in f.get("description", "").lower()
            )
            if subj_match and query_match:
                cards_column.controls.append(build_card(f))
        page.update()

    def on_search(e):
        nonlocal search_query
        search_query = e.control.value
        update_cards()

    def on_filter_click(e):
        nonlocal current_subject
        current_subject = e.control.data
        for btn in filter_buttons.controls:
            btn.style = ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE_700 if btn.data == current_subject else ft.Colors.GREY_800
            )
        page.update()
        update_cards()

    search_bar = ft.TextField(
        hint_text="Поиск формулы или темы...",
        prefix_icon=ft.Icons.SEARCH,
        on_change=on_search,
        border_radius=10,
        height=48,
        content_padding=12
    )

    subjects = ["Все", "Физика", "Химия", "Математика", "Информатика"]
    filter_buttons = ft.Row(
        wrap=True,
        spacing=8,
        controls=[
            ft.FilledButton(
                subj,
                data=subj,
                on_click=on_filter_click,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.BLUE_700 if subj == "Все" else ft.Colors.GREY_800
                )
            ) for subj in subjects
        ]
    )

    page.add(
        ft.Text("Справочник формул", size=24, weight=ft.FontWeight.BOLD),
        search_bar,
        filter_buttons,
        cards_column
    )

    update_cards()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8555))
    ft.run(main, host="0.0.0.0", port=port)