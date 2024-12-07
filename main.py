import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import pandas as pd
import os

class SQLQueryApp:
    def __init__(self, master):
        self.master = master
        master.title("SQL Query и Вставка Данных")
        master.geometry("1000x800")

        self.db_path = self.select_database()
        
        if not self.db_path:
            messagebox.showerror("Ошибка", "База данных не выбрана. Приложение будет закрыто.")
            master.quit()
            return

        try:
            self.conn = sqlite3.connect(self.db_path)
        except Exception as e:
            messagebox.showerror("Ошибка подключения", f"Не удалось подключиться к базе данных: {e}")
            master.quit()
            return
        
        self.setup_database_selection()
        self.setup_query_area()
        self.setup_insertion_area()
        self.setup_results_area()

    def select_database(self):
        """Диалог выбора файла базы данных"""
        return filedialog.askopenfilename(
            title="Выберите файл базы данных SQLite",
            filetypes=[("SQLite Database", "*.sqlite3"), ("SQLite Database", "*.db"), ("All Files", "*.*")]
        )

    def setup_database_selection(self):
        table_frame = ttk.LabelFrame(self.master, text="Выберите таблицу")
        table_frame.pack(padx=10, pady=10, fill='x')

        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]

        self.table_var = tk.StringVar()
        self.table_dropdown = ttk.Combobox(table_frame, textvariable=self.table_var, values=tables)
        self.table_dropdown.pack(padx=10, pady=10, fill='x')
        self.table_dropdown.set("Выберите таблицу")
        self.table_dropdown.bind("<<ComboboxSelected>>", self.on_table_select)

    def on_table_select(self, event):
        selected_table = self.table_var.get()
        cursor = self.conn.cursor()
        cursor.execute(f"PRAGMA table_info({selected_table})")
        columns = cursor.fetchall()
        
        self.update_insertion_fields(columns)

    def setup_query_area(self):
        query_frame = ttk.LabelFrame(self.master, text="Введите SQL-запрос")
        query_frame.pack(padx=10, pady=10, fill='both', expand=True)

        self.query_text = tk.Text(query_frame, height=5)
        self.query_text.pack(padx=10, pady=10, fill='both', expand=True)

        execute_button = ttk.Button(query_frame, text="Выполнить запрос", command=self.execute_query)
        execute_button.pack(padx=10, pady=10)

    def setup_insertion_area(self):
        insert_frame = ttk.LabelFrame(self.master, text="Вставка данных")
        insert_frame.pack(padx=10, pady=10, fill='x')

        self.insertion_fields_frame = tk.Frame(insert_frame)
        self.insertion_fields_frame.pack(padx=10, pady=10, fill='x')

        insert_button = ttk.Button(insert_frame, text="Вставить данные", command=self.insert_data)
        insert_button.pack(padx=10, pady=10)

    def update_insertion_fields(self, columns):
        for widget in self.insertion_fields_frame.winfo_children():
            widget.destroy()

        self.insertion_entries = {}
        for i, column in enumerate(columns):
            col_name = column[1]
            col_type = column[2] 

            label = ttk.Label(self.insertion_fields_frame, text=col_name)
            label.grid(row=i, column=0, padx=5, pady=5, sticky='w')
            
            entry = ttk.Entry(self.insertion_fields_frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
            
            self.insertion_entries[col_name] = entry

        self.insertion_fields_frame.columnconfigure(1, weight=1)

    def insert_data(self):
        selected_table = self.table_var.get()
        if selected_table == "Выберите таблицу":
            messagebox.showerror("Ошибка", "Пожалуйста, выберите таблицу!")
            return

        values = {}
        for col_name, entry in self.insertion_entries.items():
            value = entry.get().strip()
            if value:  
                values[col_name] = value

        columns = ', '.join(values.keys())
        placeholders = ', '.join(['?' for _ in values])
        query = f"INSERT INTO {selected_table} ({columns}) VALUES ({placeholders})"

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, list(values.values()))
            self.conn.commit()
            messagebox.showinfo("Успех", "Данные успешно добавлены!")

            for entry in self.insertion_entries.values():
                entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Ошибка вставки", str(e))

    def setup_results_area(self):
        results_frame = ttk.LabelFrame(self.master, text="Результаты")
        results_frame.pack(padx=10, pady=10, fill='both', expand=True)

        self.results_tree = ttk.Treeview(results_frame)
        self.results_tree.pack(padx=10, pady=10, fill='both', expand=True)

        scrollbar = ttk.Scrollbar(results_frame, orient='vertical', command=self.results_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.results_tree.configure(yscroll=scrollbar.set)

    def execute_query(self):
        selected_table = self.table_var.get()
        if selected_table == "Выберите таблицу":
            messagebox.showerror("Ошибка", "Пожалуйста, выберите таблицу!")
            return

        query = self.query_text.get("1.0", tk.END).strip()
        if not query:
            messagebox.showerror("Ошибка", "Введите SQL-запрос!")
            return

        try:
            df = pd.read_sql_query(query, self.conn)

            for i in self.results_tree.get_children():
                self.results_tree.delete(i)

            self.results_tree['columns'] = list(df.columns)
            self.results_tree.column("#0", width=0, stretch=tk.NO)
            
            for col in df.columns:
                self.results_tree.heading(col, text=col)
                self.results_tree.column(col, anchor=tk.CENTER, width=100)

            for index, row in df.iterrows():
                self.results_tree.insert("", tk.END, values=list(row))

        except Exception as e:
            messagebox.showerror("Ошибка выполнения запроса", str(e))

    def __del__(self):
        try:
            if hasattr(self, 'conn'):
                self.conn.close()
        except Exception:
            pass

def main():
    root = tk.Tk()
    app = SQLQueryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()