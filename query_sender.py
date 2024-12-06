import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import pandas as pd

class SQLQueryApp:
    def __init__(self, master):
        self.master = master
        master.title("SQL Query Interface")
        master.geometry("800x600")

        # Подключение к базе данных
        self.conn = sqlite3.connect('Exam/db.sqlite3')
        
        # Создание фреймов
        self.setup_database_selection()
        self.setup_query_area()
        self.setup_results_area()

    def setup_database_selection(self):
        # Фрейм для выбора таблицы
        table_frame = ttk.LabelFrame(self.master, text="Выберите таблицу")
        table_frame.pack(padx=10, pady=10, fill='x')

        # Получение списка таблиц
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]

        # Выпадающий список таблиц
        self.table_var = tk.StringVar()
        table_dropdown = ttk.Combobox(table_frame, textvariable=self.table_var, values=tables)
        table_dropdown.pack(padx=10, pady=10, fill='x')
        table_dropdown.set("Выберите таблицу")

    def setup_query_area(self):
        # Фрейм для ввода SQL-запроса
        query_frame = ttk.LabelFrame(self.master, text="Введите SQL-запрос")
        query_frame.pack(padx=10, pady=10, fill='both', expand=True)

        self.query_text = tk.Text(query_frame, height=5)
        self.query_text.pack(padx=10, pady=10, fill='both', expand=True)

        # Кнопка выполнения запроса
        execute_button = ttk.Button(query_frame, text="Выполнить запрос", command=self.execute_query)
        execute_button.pack(padx=10, pady=10)

    def setup_results_area(self):
        # Фрейм для отображения результатов
        results_frame = ttk.LabelFrame(self.master, text="Результаты")
        results_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # Создание виджета Treeview для отображения результатов
        self.results_tree = ttk.Treeview(results_frame)
        self.results_tree.pack(padx=10, pady=10, fill='both', expand=True)

        # Добавление скроллбара
        scrollbar = ttk.Scrollbar(results_frame, orient='vertical', command=self.results_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.results_tree.configure(yscroll=scrollbar.set)

    def execute_query(self):
        # Проверка выбора таблицы
        selected_table = self.table_var.get()
        if selected_table == "Выберите таблицу":
            messagebox.showerror("Ошибка", "Пожалуйста, выберите таблицу!")
            return

        # Получение SQL-запроса
        query = self.query_text.get("1.0", tk.END).strip()
        if not query:
            messagebox.showerror("Ошибка", "Введите SQL-запрос!")
            return

        try:
            # Выполнение запроса
            df = pd.read_sql_query(query, self.conn)

            # Очистка предыдущих результатов
            for i in self.results_tree.get_children():
                self.results_tree.delete(i)

            # Настройка столбцов
            self.results_tree['columns'] = list(df.columns)
            self.results_tree.column("#0", width=0, stretch=tk.NO)
            
            # Настройка заголовков
            for col in df.columns:
                self.results_tree.heading(col, text=col)
                self.results_tree.column(col, anchor=tk.CENTER, width=100)

            # Заполнение данными
            for index, row in df.iterrows():
                self.results_tree.insert("", tk.END, values=list(row))

        except Exception as e:
            messagebox.showerror("Ошибка выполнения запроса", str(e))

    def __del__(self):
        # Закрытие соединения с базой данных
        self.conn.close()

def main():
    root = tk.Tk()
    app = SQLQueryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()