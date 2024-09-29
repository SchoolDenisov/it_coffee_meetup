import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QListWidget, QLabel, 
                             QInputDialog, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt
import json
from datetime import datetime

class TodoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
        self.tasks = []
        self.completed_tasks = []
        self.emojis = ["😢", "😕", "😐", "🙂", "😄"]

    def initUI(self):
        self.setWindowTitle('To-Do Приложение')
        self.setGeometry(100, 100, 500, 600)

        layout = QVBoxLayout()

        # Ввод задачи
        input_layout = QHBoxLayout()
        self.task_entry = QLineEdit()
        self.add_button = QPushButton('Добавить задачу')
        self.add_button.clicked.connect(self.add_task)
        input_layout.addWidget(self.task_entry)
        input_layout.addWidget(self.add_button)
        layout.addLayout(input_layout)

        # Список задач
        self.task_list = QListWidget()
        layout.addWidget(self.task_list)

        # Кнопки управления задачами
        button_layout = QHBoxLayout()
        self.progress_button = QPushButton('Обновить прогресс')
        self.progress_button.clicked.connect(self.update_progress)
        self.complete_button = QPushButton('Отметить как выполненное')
        self.complete_button.clicked.connect(self.complete_task)
        button_layout.addWidget(self.progress_button)
        button_layout.addWidget(self.complete_button)
        layout.addLayout(button_layout)

        # Кнопки сохранения и загрузки
        save_load_layout = QHBoxLayout()
        self.save_button = QPushButton('Сохранить задачи')
        self.save_button.clicked.connect(self.save_tasks)
        self.load_button = QPushButton('Загрузить задачи')
        self.load_button.clicked.connect(self.load_tasks)
        save_load_layout.addWidget(self.save_button)
        save_load_layout.addWidget(self.load_button)
        layout.addLayout(save_load_layout)

        # Выполненные задачи
        layout.addWidget(QLabel('Выполненные задачи:'))
        self.completed_list = QListWidget()
        layout.addWidget(self.completed_list)

        self.setLayout(layout)

    def add_task(self):
        task = self.task_entry.text()
        if task:
            task_with_progress = {"text": task, "progress": 0}
            self.tasks.append(task_with_progress)
            self.update_task_list()
            self.task_entry.clear()
        else:
            QMessageBox.warning(self, 'Предупреждение', 'Пожалуйста, введите задачу')

    def update_task_list(self):
        self.task_list.clear()
        for task in self.tasks:
            emoji = self.emojis[task["progress"]]
            self.task_list.addItem(f"{emoji} {task['text']}")

    def update_progress(self):
        current_item = self.task_list.currentItem()
        if current_item:
            index = self.task_list.currentRow()
            task = self.tasks[index]
            progress, ok = QInputDialog.getInt(self, 'Обновить прогресс', 
                                               'Введите прогресс (1-5):', 
                                               value=task['progress']+1, 
                                               min=1, max=5)
            if ok:
                task["progress"] = progress - 1
                self.update_task_list()
        else:
            QMessageBox.warning(self, 'Предупреждение', 'Пожалуйста, выберите задачу для обновления прогресса')

    def complete_task(self):
        current_item = self.task_list.currentItem()
        if current_item:
            index = self.task_list.currentRow()
            task = self.tasks.pop(index)
            self.completed_tasks.append(task)
            self.update_task_list()
            self.completed_list.addItem(f"✅ {task['text']}")
        else:
            QMessageBox.warning(self, 'Предупреждение', 'Пожалуйста, выберите задачу для выполнения')

    def save_tasks(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Сохранить задачи', 
                                                  f"tasks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                                  'JSON files (*.json)')
        if filename:
            data = {
                "tasks": self.tasks,
                "completed_tasks": self.completed_tasks
            }
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            QMessageBox.information(self, 'Информация', f'Задачи сохранены в файл {filename}')

    def load_tasks(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Загрузить задачи', '', 'JSON files (*.json)')
        if filename:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.tasks = data.get("tasks", [])
            self.completed_tasks = data.get("completed_tasks", [])

            self.update_task_list()
            self.completed_list.clear()

            for task in self.completed_tasks:
                self.completed_list.addItem(f"✅ {task['text']}")

            QMessageBox.information(self, 'Информация', 'Задачи загружены успешно')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TodoApp()
    ex.show()
    sys.exit(app.exec_())