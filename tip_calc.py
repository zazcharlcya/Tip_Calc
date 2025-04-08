"""
Модуль для расчета чаевых с возможностью сохранения истории, экспорта данных и пересчета
в реальном времени.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import logging
import csv

# Настройка логирования
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def validate_input(value):
    """Проверяет, что введенное значение является положительным числом."""
    try:
        return float(value) > 0
    except ValueError:
        return False


def clear_fields():
    """Очищает все поля ввода и результаты."""
    entry_bill.delete(0, tk.END)
    entry_people.delete(0, tk.END)
    entry_exchange_rate.delete(0, tk.END)
    entry_exchange_rate.insert(0, "1.0")
    result_tip.set("")
    result_total.set("")
    result_per_person.set("")
    tip_var.set("10")
    split_var.set(0)
    save_var.set(0)
    toggle_split_state()


def save_to_history(bill_amount, tip_amount, total_amount):
    """Сохраняет расчет в файл JSON."""
    history = {"Счет": bill_amount, "Чаевые": tip_amount, "Общая сумма": total_amount}
    try:
        with open("tip_calculator_history.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    data.append(history)
    with open("tip_calculator_history.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def show_history():
    """Открывает окно с историей расчетов."""
    try:
        with open("tip_calculator_history.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        history_window = tk.Toplevel(app)
        history_window.title("История расчетов")
        history_window.geometry("400x300")
        history_text = tk.Text(history_window, wrap=tk.WORD)
        history_text.pack(expand=True, fill=tk.BOTH)
        for record in data:
            history_text.insert(
                tk.END,
                f"Счет: {record['Счет']} руб., Чаевые: {record['Чаевые']} руб., "
                f"Общая сумма: {record['Общая сумма']} руб.\n"
            )
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showinfo("История", "История расчетов пуста.")


def export_history():
    """Экспортирует историю расчетов в CSV-файл."""
    try:
        with open("tip_calculator_history.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        with open("tip_calculator_history.csv", "w", encoding="utf-8", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Счет", "Чаевые", "Общая сумма"])
            for record in data:
                writer.writerow([record["Счет"], record["Чаевые"], record["Общая сумма"]])
        messagebox.showinfo(
            "Экспорт",
            "История успешно экспортирована в файл tip_calculator_history.csv."
        )
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showinfo("Экспорт", "История расчетов пуста.")


def recalculate_tip():
    """Пересчитывает чаевые и общую сумму в реальном времени."""
    try:
        bill_amount = entry_bill.get()
        if not bill_amount.strip() or not validate_input(bill_amount):
            result_tip.set("")
            result_total.set("")
            result_per_person.set("")
            return
        bill_amount = float(bill_amount)

        tip_percentage = int(tip_var.get())
        tip_amount = round(bill_amount * tip_percentage / 100, 2)
        total_amount = round(bill_amount + tip_amount, 2)

        exchange_rate = entry_exchange_rate.get()
        if not exchange_rate.strip() or not validate_input(exchange_rate):
            result_tip.set("")
            result_total.set("")
            result_per_person.set("")
            return
        exchange_rate = float(exchange_rate)

        currency = currency_var.get()
        converted_tip = round(tip_amount * exchange_rate, 2)
        converted_total = round(total_amount * exchange_rate, 2)

        result_tip.set(f"Сумма чаевых: {converted_tip} {currency}")
        result_total.set(f"Общая сумма к оплате: {converted_total} {currency}")

        if split_var.get() == 1:
            num_people = entry_people.get()
            if not num_people.strip() or not validate_input(num_people):
                result_per_person.set("")
                return
            num_people = int(num_people)
            if num_people < 1:
                result_per_person.set("")
                return
            per_person_total = round(converted_total / num_people, 2)
            result_per_person.set(f"На каждого: {per_person_total} {currency}")
        else:
            result_per_person.set("")
    except ValueError:
        result_tip.set("")
        result_total.set("")
        result_per_person.set("")


def toggle_split_state():
    """Включает или отключает поле 'Количество человек' в зависимости от состояния флажка."""
    if split_var.get() == 1:
        entry_people.configure(state='normal')
    else:
        entry_people.configure(state='disabled')


def toggle_theme():
    """Переключает тему оформления."""
    current_theme = style.theme_use()
    if current_theme == "clam":
        style.theme_use("alt")
        app.configure(bg="#2e2e2e")
    else:
        style.theme_use("clam")
        app.configure(bg="#f0f8ff")


# Создание окна приложения
app = tk.Tk()
app.title("Калькулятор чаевых")
app.geometry("295x500")
app.configure(bg="#f0f8ff")
app.resizable(False, False)

style = ttk.Style()
style.theme_use('clam')

# Поля ввода
ttk.Label(app, text="Сумма счета:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_bill = ttk.Entry(app)
entry_bill.grid(row=0, column=1, padx=10, pady=5)
entry_bill.bind("<KeyRelease>", lambda event: recalculate_tip())

ttk.Label(app, text="Процент чаевых:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
tip_var = tk.StringVar(value="10")
ttk.Spinbox(app, from_=0, to=100, textvariable=tip_var, width=5).grid(row=1, column=1, padx=10, pady=5)
tip_var.trace("w", lambda *args: recalculate_tip())

split_var = tk.IntVar(value=0)
ttk.Checkbutton(app, text="Разделить счет", variable=split_var, command=toggle_split_state).grid(
    row=2, column=0, columnspan=2, pady=5
)
split_var.trace("w", lambda *args: recalculate_tip())

ttk.Label(app, text="Количество человек:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_people = ttk.Entry(app, state='disabled')
entry_people.grid(row=3, column=1, padx=10, pady=5)
entry_people.bind("<KeyRelease>", lambda event: recalculate_tip())

save_var = tk.IntVar(value=0)
ttk.Checkbutton(app, text="Сохранить расчет в историю", variable=save_var).grid(row=4, column=0, columnspan=2, pady=5)

ttk.Label(app, text="Валюта:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
currency_var = tk.StringVar(value="руб.")
ttk.OptionMenu(app, currency_var, "руб.", "USD", "EUR").grid(row=5, column=1, padx=10, pady=5)

ttk.Label(app, text="Курс валюты:").grid(row=6, column=0, padx=10, pady=5, sticky="e")
entry_exchange_rate = ttk.Entry(app)
entry_exchange_rate.grid(row=6, column=1, padx=10, pady=5)
entry_exchange_rate.insert(0, "1.0")
entry_exchange_rate.bind("<KeyRelease>", lambda event: recalculate_tip())

button_frame = ttk.Frame(app)
button_frame.grid(row=7, column=0, columnspan=2, pady=10)

ttk.Button(button_frame, text="Рассчитать", command=recalculate_tip).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(button_frame, text="Очистить", command=clear_fields).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(button_frame, text="Показать историю", command=show_history).grid(row=1, column=0, padx=5, pady=5)
ttk.Button(button_frame, text="Экспортировать историю", command=export_history).grid(row=1, column=1, padx=5, pady=5)
ttk.Button(button_frame, text="Переключить тему", command=toggle_theme).grid(row=2, column=0, columnspan=2, pady=5)

result_tip = tk.StringVar()
ttk.Label(app, textvariable=result_tip).grid(row=8, column=0, columnspan=2, pady=5)

result_total = tk.StringVar()
ttk.Label(app, textvariable=result_total).grid(row=9, column=0, columnspan=2, pady=5)

result_per_person = tk.StringVar()
ttk.Label(app, textvariable=result_per_person).grid(row=10, column=0, columnspan=2, pady=5)

app.mainloop()
