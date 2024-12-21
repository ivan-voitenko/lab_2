class View:
    def show_menu(self):
        self.show_message("\nМеню:")
        self.show_message("1. Додати рядок")
        self.show_message("2. Список таблиць")
        self.show_message("3. Показати таблицю")
        self.show_message("4. Редагувати рядок")
        self.show_message("5. Видалити рядок")
        self.show_message("6. Генерувати дані")
        self.show_message("7. Вихід")
        return input("Виберіть пункт: ")

    def show_message(self, message):
        print(message)

    def ask_continue(self):
        agree = input("Продовжити внесення змін? (y/n) ")
        return agree

    def show_tables(self, tables):
        print("Назви таблиць:")
        for table in tables:
            print(table)

    def ask_table(self):
        table_name = input("Введіть назву таблиці: ")
        return table_name

    def insert(self):
        while True:
            try:
                table = input("Введіть назву таблиці: ")
                columns = input("Введіть назви колонок (через пробіл): ").split()
                val = input("Введіть відповідні значення (через пробіл): ").split()
                if len(columns) != len(val):
                    raise ValueError("Кількість стовпців повинна бути дорівнювати кількості значень.")
                return table, columns, val
            except ValueError as e:
                print(f"Помилка: {e}")

    def update(self):
        while True:
            try:
                table = input("Введіть назву таблиці: ")
                column = input("Введіть назву колонки, яку хочете змінити: ")
                id = int(input("Введіть ID рядка, який потрібно змінити: "))
                new_value = input("Введіть нове значення: ")
                return table, column, id, new_value
            except ValueError as e:
                print(f"Помилка: {e}")

    def delete(self):
        while True:
            try:
                table = input("Введіть назву таблиці: ")
                id = int(input("Введіть ID рядка, який потрібно видалити: "))
                return table, id
            except ValueError as e:
                print(f"Помилка: {e}")

    def generate_data_input(self):
        while True:
            try:
                table_name = input("Введіть назву таблиці: ")
                num_rows = int(input("Введіть кількість рядків для генерації: "))
                return table_name, num_rows
            except ValueError as e:
                print(f"Помилка: {e}")
