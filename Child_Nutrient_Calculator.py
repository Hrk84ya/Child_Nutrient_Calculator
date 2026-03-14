import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from typing import Dict, List, Tuple
import math

# ─── Color Palette & Theme ───────────────────────────────────────────────────
COLORS = {
    "bg":           "#0f1117",
    "surface":      "#1a1d27",
    "card":         "#222636",
    "card_hover":   "#2a2f42",
    "border":       "#2e3348",
    "primary":      "#6c63ff",
    "primary_hover":"#7b73ff",
    "accent":       "#00d4aa",
    "accent_warm":  "#ff6b6b",
    "text":         "#e8e8f0",
    "text_dim":     "#8b8fa3",
    "text_muted":   "#5a5e73",
    "success":      "#00d4aa",
    "warning":      "#ffb347",
    "danger":       "#ff6b6b",
    "input_bg":     "#181b24",
    "input_border": "#2e3348",
    "input_focus":  "#6c63ff",
    "tab_bg":       "#181b24",
    "tab_active":   "#6c63ff",
}

FONTS = {
    "title":     ("Helvetica Neue", 22, "bold"),
    "subtitle":  ("Helvetica Neue", 13, "bold"),
    "heading":   ("Helvetica Neue", 15, "bold"),
    "body":      ("Helvetica Neue", 12),
    "body_sm":   ("Helvetica Neue", 11),
    "caption":   ("Helvetica Neue", 10),
    "button":    ("Helvetica Neue", 12, "bold"),
    "mono":      ("SF Mono", 11),
    "icon":      ("Helvetica Neue", 18),
}


@dataclass
class FoodItem:
    name: str
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float = 0.0
    calcium_mg: float = 0.0
    iron_mg: float = 0.0
    vitamin_a_iu: float = 0.0
    vitamin_c_mg: float = 0.0


class ChildNutritionCalculator:
    FOOD_DB = {
        'Milk': FoodItem('Milk', 103, 8, 12, 2.4, 0, 300, 0.1, 500, 0),
        'Egg': FoodItem('Egg', 155, 13, 1.1, 11, 0, 56, 1.8, 600, 0),
        'Rice': FoodItem('Rice', 130, 2.7, 28, 0.3, 0.4, 10, 0.2, 0, 0),
        'Lentils': FoodItem('Lentils', 113, 9, 20, 0.4, 8, 19, 3.3, 8, 1.5),
        'Vegetable': FoodItem('Vegetable', 85, 2, 20, 0.2, 6, 25, 0.5, 5000, 28),
        'Meat': FoodItem('Meat', 143, 26, 0, 3.5, 0, 12, 2.7, 40, 0)
    }

    DAILY_NUTRIENT_NEEDS = {
        '1-3': {'calories': 1000, 'protein_g': 13, 'carbs_g': 130, 'fiber_g': 19, 'calcium_mg': 700, 'iron_mg': 7, 'vitamin_a_iu': 1000, 'vitamin_c_mg': 15},
        '4-8': {'calories': 1400, 'protein_g': 19, 'carbs_g': 130, 'fiber_g': 25, 'calcium_mg': 1000, 'iron_mg': 10, 'vitamin_a_iu': 1333, 'vitamin_c_mg': 25},
        '9-13': {'calories': 1800, 'protein_g': 34, 'carbs_g': 130, 'fiber_g': 31, 'calcium_mg': 1300, 'iron_mg': 8, 'vitamin_a_iu': 2000, 'vitamin_c_mg': 45}
    }

    def __init__(self, name, age, gender, height_inch, weight_pound):
        self.name = name
        self.age = age
        self.gender = gender
        self.height_inch = height_inch
        self.weight_pound = weight_pound
        self.food_intake = {}
        self.nutrition_totals = {
            'calories': 0, 'protein_g': 0, 'carbs_g': 0, 'fat_g': 0,
            'fiber_g': 0, 'calcium_mg': 0, 'iron_mg': 0,
            'vitamin_a_iu': 0, 'vitamin_c_mg': 0
        }

    def calculate_bmi(self):
        if self.height_inch <= 0:
            raise ValueError("Height must be greater than zero.")
        return (self.weight_pound / (self.height_inch ** 2)) * 703

    def calculate_min_calories(self):
        if 0 <= self.age <= 2:
            return 800
        elif 2 < self.age <= 4:
            return 1400
        elif 4 < self.age <= 8:
            return 1800
        else:
            return 2200

    def calculate_nutrition(self, food_items):
        self.nutrition_totals = {k: 0 for k in self.nutrition_totals}
        self.food_intake = food_items
        for food, quantity in food_items.items():
            if food in self.FOOD_DB and quantity > 0:
                fi = self.FOOD_DB[food]
                self.nutrition_totals['calories'] += fi.calories * quantity
                self.nutrition_totals['protein_g'] += fi.protein_g * quantity
                self.nutrition_totals['carbs_g'] += fi.carbs_g * quantity
                self.nutrition_totals['fat_g'] += fi.fat_g * quantity
                self.nutrition_totals['fiber_g'] += fi.fiber_g * quantity
                self.nutrition_totals['calcium_mg'] += fi.calcium_mg * quantity
                self.nutrition_totals['iron_mg'] += fi.iron_mg * quantity
                self.nutrition_totals['vitamin_a_iu'] += fi.vitamin_a_iu * quantity
                self.nutrition_totals['vitamin_c_mg'] += fi.vitamin_c_mg * quantity
        return self.nutrition_totals

    def get_daily_recommendations(self) -> dict:
        if 1 <= self.age <= 3:
            return self.DAILY_NUTRIENT_NEEDS['1-3']
        elif 4 <= self.age <= 8:
            return self.DAILY_NUTRIENT_NEEDS['4-8']
        else:
            return self.DAILY_NUTRIENT_NEEDS['9-13']

    def get_nutrition_status(self) -> Dict[str, str]:
        status = {}
        recommendations = self.get_daily_recommendations()
        for nutrient, value in self.nutrition_totals.items():
            if nutrient in recommendations:
                rec = recommendations[nutrient]
                if value < rec * 0.7:
                    status[nutrient] = "Low"
                elif value > rec * 1.3:
                    status[nutrient] = "High"
                else:
                    status[nutrient] = "Adequate"
        return status

    def generate_meal_plan(self) -> List[Dict]:
        recommendations = self.get_daily_recommendations()
        current_intake = self.nutrition_totals
        meal_plan = []
        if current_intake['protein_g'] < recommendations['protein_g'] * 0.8:
            meal_plan.append({
                'suggestion': 'Add protein source',
                'foods': ['Eggs', 'Meat', 'Lentils'],
                'reason': f'Current protein intake ({current_intake["protein_g"]:.1f}g) is below recommended ({recommendations["protein_g"]}g)'
            })
        if current_intake['fiber_g'] < recommendations['fiber_g'] * 0.7:
            meal_plan.append({
                'suggestion': 'Add fiber-rich foods',
                'foods': ['Lentils', 'Vegetables', 'Whole grains'],
                'reason': f'Current fiber intake ({current_intake["fiber_g"]:.1f}g) is below recommended ({recommendations["fiber_g"]}g)'
            })
        if current_intake['calcium_mg'] < recommendations['calcium_mg'] * 0.7:
            meal_plan.append({
                'suggestion': 'Add calcium source',
                'foods': ['Milk', 'Cheese', 'Yogurt'],
                'reason': f'Current calcium intake ({current_intake["calcium_mg"]:.1f}mg) is below recommended ({recommendations["calcium_mg"]}mg)'
            })
        return meal_plan

    def check_nutrition_status(self, daily_calories):
        bmi = self.calculate_bmi()
        if bmi < 16:
            return "Severely Underweight"
        elif 16 < bmi <= 18.5:
            return "Underweight"
        elif 18.5 < bmi <= 25:
            return "Healthy"
        elif 25 < bmi <= 30:
            return "Overweight"
        else:
            return "Obese"


# ─── Custom Widget Helpers ────────────────────────────────────────────────────

class RoundedEntry(tk.Canvas):
    """A modern styled entry with rounded appearance."""
    def __init__(self, parent, placeholder="", width=260, **kwargs):
        super().__init__(parent, width=width, height=38, bg=COLORS["card"],
                         highlightthickness=0, **kwargs)
        self._placeholder = placeholder
        self._has_focus = False

        # Background rectangle
        self._bg_rect = self.create_rectangle(
            1, 1, width - 1, 37,
            fill=COLORS["input_bg"], outline=COLORS["input_border"], width=1
        )
        # Embedded entry
        self._entry = tk.Entry(
            self, bg=COLORS["input_bg"], fg=COLORS["text"],
            insertbackground=COLORS["text"], font=FONTS["body"],
            relief="flat", highlightthickness=0, bd=0
        )
        self.create_window(14, 19, window=self._entry, anchor="w", width=width - 28)

        # Placeholder
        self._show_placeholder()
        self._entry.bind("<FocusIn>", self._on_focus_in)
        self._entry.bind("<FocusOut>", self._on_focus_out)

    def _show_placeholder(self):
        if not self._entry.get():
            self._entry.insert(0, self._placeholder)
            self._entry.config(fg=COLORS["text_muted"])

    def _on_focus_in(self, e):
        self._has_focus = True
        self.itemconfig(self._bg_rect, outline=COLORS["input_focus"])
        if self._entry.get() == self._placeholder:
            self._entry.delete(0, tk.END)
            self._entry.config(fg=COLORS["text"])

    def _on_focus_out(self, e):
        self._has_focus = False
        self.itemconfig(self._bg_rect, outline=COLORS["input_border"])
        if not self._entry.get():
            self._show_placeholder()

    def get(self):
        val = self._entry.get()
        return "" if val == self._placeholder else val

    def delete(self, first, last):
        self._entry.delete(first, last)
        self._show_placeholder()

    def insert(self, index, string):
        self._entry.config(fg=COLORS["text"])
        self._entry.insert(index, string)


class GenderSelector(tk.Frame):
    """Styled gender toggle buttons."""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLORS["card"], **kwargs)
        self._value = tk.StringVar(value="")
        self._buttons = {}
        for i, (text, val) in enumerate([("♂  Male", "Male"), ("♀  Female", "Female")]):
            btn = tk.Label(
                self, text=text, font=FONTS["body_sm"],
                bg=COLORS["input_bg"], fg=COLORS["text_dim"],
                padx=20, pady=8, cursor="hand2"
            )
            btn.grid(row=0, column=i, padx=(0, 8))
            btn.bind("<Button-1>", lambda e, v=val: self._select(v))
            self._buttons[val] = btn

    def _select(self, val):
        self._value.set(val)
        for v, btn in self._buttons.items():
            if v == val:
                btn.config(bg=COLORS["primary"], fg="#ffffff")
            else:
                btn.config(bg=COLORS["input_bg"], fg=COLORS["text_dim"])

    def get(self):
        return self._value.get()

    def reset(self):
        self._value.set("")
        for btn in self._buttons.values():
            btn.config(bg=COLORS["input_bg"], fg=COLORS["text_dim"])


class PremiumButton(tk.Canvas):
    """Styled button with hover effects."""
    def __init__(self, parent, text, command, style="primary", width=180, **kwargs):
        height = 42
        super().__init__(parent, width=width, height=height,
                         bg=COLORS["card"], highlightthickness=0, **kwargs)
        self._command = command
        colors = {
            "primary": (COLORS["primary"], COLORS["primary_hover"], "#ffffff"),
            "secondary": (COLORS["surface"], COLORS["card_hover"], COLORS["text_dim"]),
            "danger": (COLORS["danger"], "#ff8585", "#ffffff"),
        }
        self._bg_color, self._hover_color, self._fg_color = colors.get(style, colors["primary"])

        self._rect = self.create_rectangle(
            0, 0, width, height, fill=self._bg_color, outline="", width=0
        )
        self._text = self.create_text(
            width // 2, height // 2, text=text,
            font=FONTS["button"], fill=self._fg_color
        )
        self.bind("<Enter>", lambda e: self.itemconfig(self._rect, fill=self._hover_color))
        self.bind("<Leave>", lambda e: self.itemconfig(self._rect, fill=self._bg_color))
        self.bind("<Button-1>", lambda e: self._command())


class NutrientBar(tk.Canvas):
    """Horizontal progress bar for nutrient tracking."""
    def __init__(self, parent, label, value, target, unit, width=420, **kwargs):
        super().__init__(parent, width=width, height=56, bg=COLORS["card"],
                         highlightthickness=0, **kwargs)
        pct = min(value / target, 1.5) if target > 0 else 0
        bar_width = int((width - 20) * min(pct, 1.0))

        # Determine color
        if pct < 0.7:
            color = COLORS["danger"]
            status = "Low"
        elif pct > 1.3:
            color = COLORS["warning"]
            status = "High"
        else:
            color = COLORS["success"]
            status = "Good"

        # Label row
        self.create_text(10, 12, text=label, anchor="w",
                         font=FONTS["body_sm"], fill=COLORS["text"])
        self.create_text(width - 10, 12, text=f"{value:.1f} / {target:.0f} {unit}",
                         anchor="e", font=FONTS["caption"], fill=COLORS["text_dim"])

        # Status badge
        badge_x = width - 10
        self.create_text(badge_x, 12, text="", anchor="e")

        # Track background
        self.create_rectangle(10, 28, width - 10, 40,
                              fill=COLORS["input_bg"], outline="")
        # Filled bar
        if bar_width > 0:
            self.create_rectangle(10, 28, 10 + bar_width, 40,
                                  fill=color, outline="")

        # Percentage text
        self.create_text(10, 50, text=f"{pct * 100:.0f}% of daily target  •  {status}",
                         anchor="w", font=FONTS["caption"], fill=COLORS["text_muted"])


# ─── Main Application ────────────────────────────────────────────────────────

class NutritionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NutriKid  —  Child Nutrition Calculator")
        self.root.geometry("580x860")
        self.root.configure(bg=COLORS["bg"])
        self.root.minsize(540, 700)

        # ── Scrollable container ──
        self.outer = tk.Frame(root, bg=COLORS["bg"])
        self.outer.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.outer, bg=COLORS["bg"], highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.outer, orient="vertical",
                                       command=self.canvas.yview,
                                       bg=COLORS["bg"], troughcolor=COLORS["bg"])
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.container = tk.Frame(self.canvas, bg=COLORS["bg"])
        self.canvas_window = self.canvas.create_window((0, 0), window=self.container, anchor="nw")

        self.container.bind("<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self._on_canvas_resize)

        # Mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>",
            lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        self.entries = {}
        self._build_ui()

    def _on_canvas_resize(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    # ── Card helper ──
    def _card(self, parent, **kwargs):
        f = tk.Frame(parent, bg=COLORS["card"], padx=24, pady=20, **kwargs)
        f.pack(fill="x", padx=20, pady=(0, 12))
        return f

    def _section_label(self, parent, icon, text):
        row = tk.Frame(parent, bg=COLORS["card"])
        row.pack(fill="x", pady=(0, 14))
        tk.Label(row, text=icon, font=FONTS["icon"], bg=COLORS["card"],
                 fg=COLORS["primary"]).pack(side="left")
        tk.Label(row, text=text, font=FONTS["heading"], bg=COLORS["card"],
                 fg=COLORS["text"]).pack(side="left", padx=(8, 0))

    def _field_row(self, parent, label, placeholder="", key=None):
        row = tk.Frame(parent, bg=COLORS["card"])
        row.pack(fill="x", pady=(0, 8))
        tk.Label(row, text=label, font=FONTS["body_sm"], bg=COLORS["card"],
                 fg=COLORS["text_dim"], width=16, anchor="w").pack(side="left")
        entry = RoundedEntry(row, placeholder=placeholder, width=260)
        entry.pack(side="left", padx=(4, 0))
        self.entries[key or label] = entry
        return entry

    # ── Build the full UI ──
    def _build_ui(self):
        pad = tk.Frame(self.container, bg=COLORS["bg"], height=16)
        pad.pack(fill="x")

        # ── Header ──
        header = tk.Frame(self.container, bg=COLORS["bg"])
        header.pack(fill="x", padx=24, pady=(8, 16))
        tk.Label(header, text="🥗", font=("Helvetica Neue", 28),
                 bg=COLORS["bg"]).pack(side="left")
        title_col = tk.Frame(header, bg=COLORS["bg"])
        title_col.pack(side="left", padx=(12, 0))
        tk.Label(title_col, text="NutriKid", font=FONTS["title"],
                 bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor="w")
        tk.Label(title_col, text="Smart nutrition tracking for growing kids",
                 font=FONTS["caption"], bg=COLORS["bg"],
                 fg=COLORS["text_muted"]).pack(anchor="w")

        # ── Personal Info Card ──
        card1 = self._card(self.container)
        self._section_label(card1, "👤", "Personal Information")
        self._field_row(card1, "Name", "Enter child's name", "Name")
        self._field_row(card1, "Age (years)", "e.g. 5", "Age (years)")

        # Gender selector
        grow = tk.Frame(card1, bg=COLORS["card"])
        grow.pack(fill="x", pady=(0, 8))
        tk.Label(grow, text="Gender", font=FONTS["body_sm"], bg=COLORS["card"],
                 fg=COLORS["text_dim"], width=16, anchor="w").pack(side="left")
        self.gender_selector = GenderSelector(grow)
        self.gender_selector.pack(side="left", padx=(4, 0))

        self._field_row(card1, "Height (in)", "e.g. 42", "Height (inches)")
        self._field_row(card1, "Weight (lbs)", "e.g. 45", "Weight (pounds)")

        # ── Food Intake Card ──
        card2 = self._card(self.container)
        self._section_label(card2, "🍽️", "Daily Food Intake")

        food_fields = [
            ("Milk (cups)", "0", "Milk"),
            ("Eggs (count)", "0", "Eggs"),
            ("Rice (cups)", "0", "Rice"),
            ("Lentils (cups)", "0", "Lentils"),
            ("Vegetables (cups)", "0", "Vegetables"),
            ("Meat (oz)", "0", "Meat"),
        ]
        for label, ph, key in food_fields:
            self._field_row(card2, label, ph, key)

        # ── Buttons ──
        btn_row = tk.Frame(self.container, bg=COLORS["bg"])
        btn_row.pack(fill="x", padx=20, pady=(4, 12))
        PremiumButton(btn_row, "✦  Calculate Nutrition", self.calculate,
                      style="primary", width=260).pack(side="left", padx=(0, 8))
        PremiumButton(btn_row, "Clear", self.clear_form,
                      style="secondary", width=120).pack(side="left")

        # ── Results area (tabs) ──
        self.results_container = tk.Frame(self.container, bg=COLORS["bg"])
        self.results_container.pack(fill="x", padx=20, pady=(0, 20))

        # Tab bar
        self.tab_bar = tk.Frame(self.results_container, bg=COLORS["tab_bg"])
        self.tab_bar.pack(fill="x")

        self._tabs = {}
        self._tab_buttons = {}
        self._active_tab = None

        for tab_id, label in [("summary", "Summary"), ("details", "Nutrition Details"), ("meal", "Meal Plan")]:
            btn = tk.Label(
                self.tab_bar, text=label, font=FONTS["body_sm"],
                bg=COLORS["tab_bg"], fg=COLORS["text_muted"],
                padx=18, pady=10, cursor="hand2"
            )
            btn.pack(side="left")
            btn.bind("<Button-1>", lambda e, t=tab_id: self._switch_tab(t))
            self._tab_buttons[tab_id] = btn

            frame = tk.Frame(self.results_container, bg=COLORS["card"], padx=20, pady=16)
            self._tabs[tab_id] = frame

        # Initialize text widgets inside each tab
        self.summary_frame = self._tabs["summary"]
        self.details_frame = self._tabs["details"]
        self.meal_frame = self._tabs["meal"]

        self._switch_tab("summary")

    def _switch_tab(self, tab_id):
        if self._active_tab == tab_id:
            return
        # Hide all
        for tid, frame in self._tabs.items():
            frame.pack_forget()
            self._tab_buttons[tid].config(bg=COLORS["tab_bg"], fg=COLORS["text_muted"])
        # Show selected
        self._tabs[tab_id].pack(fill="x")
        self._tab_buttons[tab_id].config(bg=COLORS["primary"], fg="#ffffff")
        self._active_tab = tab_id

    def clear_form(self):
        for key, entry in self.entries.items():
            entry.delete(0, tk.END)
        self.gender_selector.reset()
        # Clear result frames
        for frame in self._tabs.values():
            for w in frame.winfo_children():
                w.destroy()

    def calculate(self):
        try:
            name = self.entries["Name"].get()
            age = int(self.entries["Age (years)"].get() or 0)
            gender = self.gender_selector.get()
            height = float(self.entries["Height (inches)"].get() or 0)
            weight = float(self.entries["Weight (pounds)"].get() or 0)

            if not all([name, age > 0, height > 0, weight > 0]):
                raise ValueError("Please fill in all required fields with valid values.")

            food_items = {
                "Milk": float(self.entries["Milk"].get() or 0),
                "Egg": float(self.entries["Eggs"].get() or 0),
                "Rice": float(self.entries["Rice"].get() or 0),
                "Lentils": float(self.entries["Lentils"].get() or 0),
                "Vegetable": float(self.entries["Vegetables"].get() or 0),
                "Meat": float(self.entries["Meat"].get() or 0),
            }

            calculator = ChildNutritionCalculator(name, age, gender, height, weight)
            bmi = calculator.calculate_bmi()
            min_calories = calculator.calculate_min_calories()
            nutrition = calculator.calculate_nutrition(food_items)
            status = calculator.check_nutrition_status(nutrition['calories'])
            meal_plan = calculator.generate_meal_plan()

            self._show_summary(name, bmi, min_calories, nutrition, status)
            self._show_details(nutrition, calculator)
            self._show_meal_plan(meal_plan)
            self._switch_tab("summary")

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    # ── Summary Tab ──
    def _show_summary(self, name, bmi, min_calories, nutrition, status):
        frame = self.summary_frame
        for w in frame.winfo_children():
            w.destroy()

        # Status color
        status_colors = {
            "Healthy": COLORS["success"], "Underweight": COLORS["warning"],
            "Severely Underweight": COLORS["danger"], "Overweight": COLORS["warning"],
            "Obese": COLORS["danger"],
        }
        sc = status_colors.get(status, COLORS["text_dim"])

        # Name header
        tk.Label(frame, text=f"{name}'s Nutrition Report", font=FONTS["heading"],
                 bg=COLORS["card"], fg=COLORS["text"]).pack(anchor="w", pady=(0, 12))

        # Stat cards row
        stats_row = tk.Frame(frame, bg=COLORS["card"])
        stats_row.pack(fill="x", pady=(0, 16))

        for i, (label, value, color) in enumerate([
            ("BMI", f"{bmi:.1f}", sc),
            ("Status", status, sc),
            ("Calories", f"{nutrition['calories']:.0f}", COLORS["primary"]),
            ("Target", f"{min_calories}", COLORS["text_dim"]),
        ]):
            cell = tk.Frame(stats_row, bg=COLORS["surface"], padx=12, pady=10)
            cell.pack(side="left", expand=True, fill="x", padx=(0 if i == 0 else 6, 0))
            tk.Label(cell, text=label, font=FONTS["caption"],
                     bg=COLORS["surface"], fg=COLORS["text_muted"]).pack(anchor="w")
            tk.Label(cell, text=value, font=FONTS["subtitle"],
                     bg=COLORS["surface"], fg=color).pack(anchor="w")

        # Calorie status message
        if nutrition['calories'] < min_calories * 0.9:
            cal_msg = "⚠  Calorie intake is below the recommended level"
            cal_color = COLORS["warning"]
        elif nutrition['calories'] > min_calories * 1.1:
            cal_msg = "⚠  Calorie intake exceeds the recommended level"
            cal_color = COLORS["warning"]
        else:
            cal_msg = "✓  Calorie intake is within the recommended range"
            cal_color = COLORS["success"]

        msg_frame = tk.Frame(frame, bg=COLORS["surface"], padx=14, pady=10)
        msg_frame.pack(fill="x", pady=(0, 12))
        tk.Label(msg_frame, text=cal_msg, font=FONTS["body_sm"],
                 bg=COLORS["surface"], fg=cal_color).pack(anchor="w")

        # Macros summary
        tk.Label(frame, text="Macronutrients", font=FONTS["subtitle"],
                 bg=COLORS["card"], fg=COLORS["text"]).pack(anchor="w", pady=(4, 8))

        macros = [
            ("Protein", nutrition['protein_g'], "g", COLORS["primary"]),
            ("Carbs", nutrition['carbs_g'], "g", COLORS["accent"]),
            ("Fats", nutrition['fat_g'], "g", COLORS["accent_warm"]),
        ]
        macro_row = tk.Frame(frame, bg=COLORS["card"])
        macro_row.pack(fill="x")
        for label, val, unit, color in macros:
            cell = tk.Frame(macro_row, bg=COLORS["surface"], padx=14, pady=10)
            cell.pack(side="left", expand=True, fill="x", padx=(0, 6))
            tk.Label(cell, text=label, font=FONTS["caption"],
                     bg=COLORS["surface"], fg=COLORS["text_muted"]).pack(anchor="w")
            tk.Label(cell, text=f"{val:.1f}{unit}", font=FONTS["subtitle"],
                     bg=COLORS["surface"], fg=color).pack(anchor="w")

    # ── Details Tab ──
    def _show_details(self, nutrition, calculator):
        frame = self.details_frame
        for w in frame.winfo_children():
            w.destroy()

        recommendations = calculator.get_daily_recommendations()

        tk.Label(frame, text="Nutrient Breakdown", font=FONTS["heading"],
                 bg=COLORS["card"], fg=COLORS["text"]).pack(anchor="w", pady=(0, 6))
        tk.Label(frame, text="Progress toward daily recommended intake",
                 font=FONTS["caption"], bg=COLORS["card"],
                 fg=COLORS["text_muted"]).pack(anchor="w", pady=(0, 14))

        nutrients = [
            ("Protein", "protein_g", "g"),
            ("Carbohydrates", "carbs_g", "g"),
            ("Fiber", "fiber_g", "g"),
            ("Calcium", "calcium_mg", "mg"),
            ("Iron", "iron_mg", "mg"),
            ("Vitamin A", "vitamin_a_iu", "IU"),
            ("Vitamin C", "vitamin_c_mg", "mg"),
        ]
        for label, key, unit in nutrients:
            val = nutrition.get(key, 0)
            target = recommendations.get(key, 1)
            bar = NutrientBar(frame, label, val, target, unit, width=420)
            bar.pack(fill="x", pady=(0, 4))

    # ── Meal Plan Tab ──
    def _show_meal_plan(self, meal_plan):
        frame = self.meal_frame
        for w in frame.winfo_children():
            w.destroy()

        tk.Label(frame, text="Meal Plan Suggestions", font=FONTS["heading"],
                 bg=COLORS["card"], fg=COLORS["text"]).pack(anchor="w", pady=(0, 12))

        if not meal_plan:
            ok_frame = tk.Frame(frame, bg=COLORS["surface"], padx=16, pady=14)
            ok_frame.pack(fill="x")
            tk.Label(ok_frame, text="✓  Your current diet meets the basic nutritional recommendations.",
                     font=FONTS["body_sm"], bg=COLORS["surface"],
                     fg=COLORS["success"], wraplength=380, justify="left").pack(anchor="w")
            return

        for i, item in enumerate(meal_plan):
            card = tk.Frame(frame, bg=COLORS["surface"], padx=16, pady=12)
            card.pack(fill="x", pady=(0, 8))

            tk.Label(card, text=f"{i+1}.  {item['suggestion']}", font=FONTS["subtitle"],
                     bg=COLORS["surface"], fg=COLORS["text"]).pack(anchor="w")
            tk.Label(card, text=f"Try: {', '.join(item['foods'])}",
                     font=FONTS["body_sm"], bg=COLORS["surface"],
                     fg=COLORS["accent"]).pack(anchor="w", pady=(4, 2))
            tk.Label(card, text=item['reason'], font=FONTS["caption"],
                     bg=COLORS["surface"], fg=COLORS["text_muted"],
                     wraplength=380, justify="left").pack(anchor="w")

        # Tips
        tips_frame = tk.Frame(frame, bg=COLORS["surface"], padx=16, pady=12)
        tips_frame.pack(fill="x", pady=(8, 0))
        tk.Label(tips_frame, text="💡  General Tips", font=FONTS["subtitle"],
                 bg=COLORS["surface"], fg=COLORS["text"]).pack(anchor="w", pady=(0, 6))
        tips = [
            "Include colorful fruits and vegetables daily",
            "Choose whole grains over refined grains",
            "Stay hydrated with plenty of water",
            "Limit added sugars and processed foods",
        ]
        for tip in tips:
            tk.Label(tips_frame, text=f"  •  {tip}", font=FONTS["caption"],
                     bg=COLORS["surface"], fg=COLORS["text_dim"]).pack(anchor="w", pady=1)


def main():
    root = tk.Tk()
    app = NutritionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
