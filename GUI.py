import os
from openai import OpenAI
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel

class FundraisingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.goal_input = QLineEdit(self)
        self.goal_input.setPlaceholderText("Введіть мету збору коштів")
        layout.addWidget(self.goal_input)

        self.classify_button = QPushButton("Отримати категорію", self)
        self.classify_button.clicked.connect(self.get_category)
        layout.addWidget(self.classify_button)

        self.result_label = QLabel(self)
        layout.addWidget(self.result_label)

        self.setLayout(layout)
        self.setWindowTitle("Класифікатор збору коштів")

    def get_category(self):
        goal_text = self.goal_input.text()
        if not goal_text.strip():
            self.result_label.setText("Будь ласка, введіть мету.")
            return

        category = get_gpt_classification(goal_text)
        self.result_label.setText(f"Категорія: {category}")
