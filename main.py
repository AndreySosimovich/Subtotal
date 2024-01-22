import csv
import os
from datetime import datetime
from tabulate import tabulate


class Note:
    def __init__(self, id, title, body, created, last_modified):
        self.id = id
        self.title = title
        self.body = body
        self.created = created
        self.last_modified = last_modified

class LoadNotes:
    @staticmethod
    def execute():
        if os.path.exists(NOTES_FILE):
            with open(NOTES_FILE, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file, delimiter=";")
                return [Note(**row) for row in reader]
        return []

class SaveNotes:
    @staticmethod
    def execute(notes):
        with open(NOTES_FILE, "w", newline="", encoding="utf-8") as file:
            fieldnames = ["id", "title", "body", "created", "last_modified"]
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            for note in notes:
                writer.writerow(vars(note))

class DisplayNotes:
    @staticmethod
    def execute(notes):
        if not notes:
            print("Нет доступных заметок.")
            return

        sorted_notes = sorted(notes, key=lambda x: x.created)
        headers = ["ID", "Title", "Body", "Created", "Last Modified"]
        table_data = [[note.id, note.title, note.body, note.created, note.last_modified] for note in sorted_notes]

        print(tabulate(table_data, headers=headers, tablefmt="grid", colalign=["center"] * len(headers)))
        
class FilterNotesByDate:
    @staticmethod
    def execute(note_manager):
        date_str = input("Введите дату в формате YYYY-MM-DD для выборки заметок: ")

        try:
            filter_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Некорректный формат даты.")
            return

        filtered_notes = [note for note in note_manager.notes if datetime.strptime(note.created, "%Y-%m-%d %H:%M:%S").date() == filter_date]

        if not filtered_notes:
            print(f"Нет заметок, созданных {date_str}.")
            return

        headers = ["ID", "Title", "Body", "Created", "Last Modified"]
        table_data = [[note.id, note.title, note.body, note.created, note.last_modified] for note in filtered_notes]

        print(tabulate(table_data, headers=headers, tablefmt="grid"))        

class NoteManager:
    def __init__(self):
        self.notes = LoadNotes.execute()

    def display_notes(self):
        DisplayNotes.execute(self.notes)

    def save_notes(self):
        SaveNotes.execute(self.notes)

class AddNote:
    @staticmethod
    def execute(note_manager):
        new_id = input("Введите номер заметки (целое число, от 1 до 9999): ")
        
        if any(note.id == str(new_id) for note in note_manager.notes):
            print(f"Заметка с номером {new_id} уже существует.")
            return

        if not new_id.isdigit():
            print("Некорректный ввод. Номер должен быть целым числом.")
            return

        new_id = int(new_id)

        if not (1 <= new_id <= 9999):
            print("Некорректный ввод. Номер должен быть положительным числом, не превышающим 9999.")
            return

        title = input("Введите название заметки: ")
        body = input("Введите текст заметки: ")

        new_note = Note(
            id=str(new_id),
            title=title,
            body=body,
            created=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            last_modified=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        note_manager.notes.append(new_note)
        print("Заметка добавлена:")
        print(vars(new_note))

        note_manager.save_notes()  # Сохраняем заметки сразу после добавления новой заметки

class EditNote:
    @staticmethod
    def execute(note_manager):
        note_id = input("Введите номер заметки, которую хотите отредактировать: ")

        if not note_id.isdigit():
            print("Некорректный ввод. Номер должен быть целым числом.")
            return

        note_id = int(note_id)

        note_to_edit = next((note for note in note_manager.notes if note.id == str(note_id)), None)

        if note_to_edit:
            print("Текущая заметка:")
            print(vars(note_to_edit))

            new_title = input("Введите новое название (или ничего не вводите для сохранения текущего): ")
            if new_title:
                note_to_edit.title = new_title

            new_body = input("Введите новый текст (или ничего не вводите для сохранения текущего): ")
            if new_body:
                note_to_edit.body = new_body

            note_to_edit.last_modified = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("Заметка успешно отредактирована:")
            print(vars(note_to_edit))

            note_manager.save_notes()  # Сохраняем заметки после редактирования
        else:
            print(f"Заметка с номером {note_id} не найдена.")
            
class DeleteNote:
    @staticmethod
    def execute(note_manager):
        note_id = input("Введите номер заметки, которую хотите удалить: ")

        if not note_id.isdigit():
            print("Некорректный ввод. Номер должен быть целым числом.")
            return

        note_id = int(note_id)

        note_found = False
        for note in note_manager.notes:
            if note.id == str(note_id):
                note_manager.notes.remove(note)
                note_found = True
                print(f"Заметка с номером {note_id} удалена.")
                note_manager.save_notes()  # Сохраняем заметки после удаления
                break

        if not note_found:
            print(f"Заметка с номером {note_id} не найдена.")
            
class ViewNoteById:
    @staticmethod
    def execute(note_manager):
        note_id = input("Введите номер заметки для просмотра: ")

        if not note_id.isdigit():
            print("Некорректный ввод. Номер должен быть целым числом.")
            return

        note_id = int(note_id)

        note_to_view = next((note for note in note_manager.notes if note.id == str(note_id)), None)

        if note_to_view:
            headers = ["ID", "Title", "Body", "Created", "Last Modified"]
            table_data = [[note_to_view.id, note_to_view.title, note_to_view.body, note_to_view.created, note_to_view.last_modified]]

            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            print(f"Заметка с номером {note_id} не найдена.")
            
class SearchNotesByBody:
    @staticmethod
    def execute(note_manager):
        search_text = input("Введите текст для поиска по содержанию: ")

        matching_notes = [note for note in note_manager.notes if search_text.lower() in note.body.lower()]

        if not matching_notes:
            print(f"Нет заметок, содержащих текст '{search_text}'.")
            return

        headers = ["ID", "Title", "Body", "Created", "Last Modified"]
        table_data = [[note.id, note.title, note.body, note.created, note.last_modified] for note in matching_notes]

        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        
class SearchNotesByTitle:
    @staticmethod
    def execute(note_manager):
        search_text = input("Введите текст для поиска по названиям заметок: ")

        matching_notes = [note for note in note_manager.notes if search_text.lower() in note.title.lower()]

        if not matching_notes:
            print(f"Нет заметок с названиями, содержащими текст '{search_text}'.")
            return

        headers = ["ID", "Title", "Body", "Created", "Last Modified"]
        table_data = [[note.id, note.title, note.body, note.created, note.last_modified] for note in matching_notes]

        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        
class Menu:
    def __init__(self):
        self.note_manager = NoteManager()

    def display_menu(self):
        print("\nЧем займемся?:")
        print("1. Создать")
        print("2. Поиск")
        print("3. Редактирование")
        print("4. Удаление")
        print("5. Выйти из программы")

    def execute_menu(self):
        while True:
            self.display_menu()

            choice = input()

            if choice == "1":
                AddNote.execute(self.note_manager)
            elif choice == "2":
                self.execute_view_search_menu()
            elif choice == "3":
                EditNote.execute(self.note_manager)
            elif choice == "4":
                DeleteNote.execute(self.note_manager)
            elif choice == "5":
                break
            else:
                print("Некорректный ввод. Пожалуйста, выберите число от 1 до 5.")

    def execute_view_search_menu(self):
        while True:
            print("\nВыберите опцию просмотра и поиска заметок:")
            print("1. Просмотр всех заметок")
            print("2. Поиск по дате создания")
            print("3. Поиск по содержанию")
            print("4. Поиск по названию")
            print("5. Поиск по номеру")
            print("6. Вернуться в предыдущее меню")
            print("7. Выйти из программы")

            view_search_choice = input()

            if view_search_choice == "1":
                self.note_manager.display_notes()
            elif view_search_choice == "2":
                FilterNotesByDate.execute(self.note_manager)
            elif view_search_choice == "3":
                SearchNotesByBody.execute(self.note_manager)
            elif view_search_choice == "4":
                SearchNotesByTitle.execute(self.note_manager)
            elif view_search_choice == "5":
                ViewNoteById.execute(self.note_manager)
            elif view_search_choice == "6":
                break
            elif view_search_choice == "7":
                 exit()
            else:
                print("Некорректный выбор опции.")
if __name__ == "__main__":
    NOTES_FILE = "notes.csv"
    menu = Menu()
    menu.execute_menu()

