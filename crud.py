import json
from datetime import datetime


def log_activity(func):
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Вызван метод {func.__name__} с аргументами {args} {kwargs}")
        return func(*args, **kwargs)

    return wrapper


class Task:
    def __init__(self, name, ds, status, data):
        self.name = name
        self.ds = ds
        self.status = status
        self.data = data

    @log_activity
    def mark_as_done(self):
        self.status = "выполнено"

    @log_activity
    def mark_as_undone(self):
        self.status = "не выполнено"

    @log_activity
    def edit_description(self, new_ds):
        self.ds = new_ds

    def __str__(self):
        return f"Задача: {self.name}\nОписание: {self.ds}\nСтатус: {self.status}\nДата создания: {self.data}"


class TaskList:
    def __init__(self):
        self.tasks = []

    @log_activity
    def create_task(self, task):
        self.tasks.append(task)

    @log_activity
    def get_task(self, index):
        if 0 <= index < len(self.tasks):
            return self.tasks[index]
        else:
            print("Недопустимый индекс задачи.")
            return None

    @log_activity
    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            removed_task = self.tasks.pop(index)
            return removed_task
        else:
            print("Недопустимый индекс задачи.")
            return None

    @log_activity
    def get_all_tasks(self):
        return self.tasks

    def __len__(self):
        return len(self.tasks)


def save_data(task_list):
    data = []
    for task in task_list.get_all_tasks():
        task_data = {
            "название": task.name,
            "описание": task.ds,
            "статус": task.status,
            "дата создания": task.data
        }
        data.append(task_data)

    with open("tasks.json", "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_data(task_list):
    try:
        with open("tasks.json", "r") as file:
            data = json.load(file)
            for task_data in data:
                task = Task(
                    task_data["название"],
                    task_data["описание"],
                    task_data["статус"],
                    task_data["дата создания"]
                )
                task_list.create_task(task)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Файл данных не найден или содержит некорректные данные. Создан новый список задач.")


def display_tasks(task_list):
    if len(task_list) == 0:
        print("Список задач пуст.")
    else:
        for index, task in enumerate(task_list.get_all_tasks(), start=1):
            print(f"Задача #{index}")
            print(task)
            print()


def create_task_interface(task_list):
    name = input("Введите название задачи: ")
    description = input("Введите описание задачи: ")
    status = input("Введите статус задачи (выполнено/не выполнено): ")
    date_created = input("Введите дату создания задачи: ")

    task = Task(name, description, status, date_created)
    task_list.create_task(task)
    print("Задача успешно добавлена.")


def edit_task_description_interface(task_list):
    index = int(input("Введите индекс задачи для редактирования описания: ")) - 1
    task = task_list.get_task(index)
    if task is not None:
        new_description = input("Введите новое описание задачи: ")
        task.edit_description(new_description)
        print("Описание задачи успешно изменено.")


def mark_task_as_done_interface(task_list):
    index = int(input("Введите индекс задачи для установки статуса 'выполнено': ")) - 1
    task = task_list.get_task(index)
    if task is not None:
        task.mark_as_done()
        print("Статус задачи успешно изменен на 'выполнено'.")


def mark_task_as_undone_interface(task_list):
    index = int(input("Введите индекс задачи для установки статуса 'не выполнено': ")) - 1
    task = task_list.get_task(index)
    if task is not None:
        task.mark_as_undone()
        print("Статус задачи успешно изменен на 'не выполнено'.")


def remove_task_interface(task_list):
    index = int(input("Введите индекс задачи для удаления: ")) - 1
    removed_task = task_list.remove_task(index)
    if removed_task is not None:
        print("Задача успешно удалена.")
        print(removed_task)
    else:
        print("Удаление задачи не выполнено.")


def main():
    task_list = TaskList()
    load_data(task_list)

    while True:
        print("1. Создать задачу")
        print("2. Отобразить все задачи")
        print("3. Редактировать описание задачи")
        print("4. Установить статус 'выполнено'")
        print("5. Установить статус 'не выполнено'")
        print("6. Удалить задачу")
        print("0. Выход")

        choice = input("Выберите действие: ")
        print()

        if choice == "1":
            create_task_interface(task_list)
        elif choice == "2":
            display_tasks(task_list)
        elif choice == "3":
            edit_task_description_interface(task_list)
        elif choice == "4":
            mark_task_as_done_interface(task_list)
        elif choice == "5":
            mark_task_as_undone_interface(task_list)
        elif choice == "6":
            remove_task_interface(task_list)
        elif choice == "0":
            save_data(task_list)
            break
        else:
            print("Недопустимый выбор. Попробуйте снова.")


