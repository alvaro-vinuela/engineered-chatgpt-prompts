"""
This is a simple PyQt5 GUI application that allows to create elaborated
chatgtp prompts. Using a specified goal, the input text is processed
by the chatgpt model to generate the output text.
"""

import asyncio
import os
import sys

import openai
from dotenv import load_dotenv, find_dotenv
from PyQt5.QtWidgets import (QApplication,  # pylint: disable=no-name-in-module
                             QWidget,
                             QVBoxLayout,
                             QHBoxLayout,
                             QLabel,
                             QFileDialog,
                             QTextEdit,
                             QPushButton)

_ = load_dotenv(find_dotenv())  # read local .env file

openai.api_key = os.getenv('OPENAI_API_KEY')
openai.organization = os.getenv('OPENAI_ORGANIZATION')
response = ""

print("OpenAI version:", openai.__version__)


# def get_completion(prompt, model="gpt-3.5-turbo"):
async def get_completion(prompt,
                         model="gpt-3.5-turbo"):
    """
    method to query openai API
    """
    messages = [{"role": "user", "content": prompt}]
    chat = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0,
            # stream=True,
            # this is the randomness degree of the model's output
        )


    global response
    response = chat.choices[0].message["content"]
    sys.stdout.write(f"\r{response}>")
    sys.stdout.flush()
    return response


class EngineeredChatgptPrompts(
    QWidget):  # pylint: disable=too-many-instance-attributes
    """
    class to hold widgets and process method of main application
    """

    def __init__(self):
        super().__init__()

        # Create widgets
        self.goal_label = QLabel('Enter Goal:')
        self.goal_text = QTextEdit()
        self.clear_goal_button = QPushButton('Clear')
        self.load_goal_button = QPushButton('Load')
        self.save_goal_button = QPushButton('Save')
        self.input_text_label = QLabel('Enter input text:')
        self.input_text = QTextEdit()
        self.clear_input_button = QPushButton('Clear input')
        self.process_button = QPushButton('Process')
        self.result_label = QLabel('Processed Text:')
        self.output_text = QTextEdit()

        height = 400
        output_text_height = 200
        width = 800
        self.goal_text.setFixedSize(width, 70)
        self.input_text.setFixedSize(width, height)
        self.output_text.setFixedSize(width, output_text_height)
        # Enable word wrap for both text input and result label
        self.goal_text.setLineWrapMode(QTextEdit.WidgetWidth)
        self.input_text.setLineWrapMode(QTextEdit.WidgetWidth)
        self.output_text.setLineWrapMode(QTextEdit.WidgetWidth)
        self.output_text.setReadOnly(True)

        # set horizontal layouts (for buttons)
        self.goal_buttons_layout = QHBoxLayout()
        self.goal_buttons_layout.addWidget(self.clear_goal_button)
        self.goal_buttons_layout.addWidget(self.load_goal_button)
        self.goal_buttons_layout.addWidget(self.save_goal_button)
        self.process_buttons_layout = QHBoxLayout()
        self.process_buttons_layout.addWidget(self.clear_input_button)
        self.process_buttons_layout.addWidget(self.process_button)

        # Set up main main_layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.goal_label)
        main_layout.addWidget(self.goal_text)
        main_layout.addLayout(self.goal_buttons_layout)
        main_layout.addWidget(self.input_text_label)
        main_layout.addWidget(self.input_text)
        main_layout.addLayout(self.process_buttons_layout)
        main_layout.addWidget(self.result_label)
        main_layout.addWidget(self.output_text)

        # Set the main_layout for the main window
        self.setLayout(main_layout)

        # Connect the button click event to the process_text method
        self.load_goal_button.clicked.connect(self.load_goal)
        self.save_goal_button.clicked.connect(self.save_goal)
        self.clear_goal_button.clicked.connect(self.clear_goal)
        self.process_button.clicked.connect(self.process_text)
        self.clear_input_button.clicked.connect(self.clear_input)

        # Set up the main window
        self.setWindowTitle('engineered chatgpt prompts')
        self.show()

    def process_text(self):
        """ send engineered prompt to openai API and set result on output """
        input_text = self.input_text.toPlainText()
        goal = self.goal_text.toPlainText()
        # Perform processing on the input text (replace with your own logic)
        if len(goal) < 2:
            goal = "summarize in 2 sentence"
        complete_prompt = (f"with the following goal "
                           f"(delimited by triple backticks): ```{goal}```"
                           f"process the following text with specified goal"
                           f"(delimited by triple backticks): ```{input_text}```")
        asyncio.run(get_completion(complete_prompt))
        global response
        self.output_text.setPlainText(response)

    def load_goal(self):
        """ open a dialog inspecting text files on file system """
        filename = QFileDialog.getOpenFileName(self,
                                               'Open File',
                                               '.',
                                               'Text Files (*.txt)')
        if filename[0]:
            with open(filename[0], 'r', encoding='utf-8') as f:
                file_text = f.read()
                self.goal_text.setText(file_text)

    def save_goal(self):
        """ save goal text into system file """
        filename = QFileDialog.getSaveFileName(self,
                                               'Save File',
                                               '.',
                                               'Text Files (*.txt)')
        if filename[0]:
            with open(filename[0], 'w', encoding='utf-8') as f:
                my_text = self.goal_text.toPlainText()
                f.write(my_text)

    def clear_goal(self):
        """ clean goal text box """
        self.goal_text.setText('')

    def clear_input(self):
        """ clean input text box """
        self.input_text.setText('')


if __name__ == '__main__':
    app = QApplication([])
    window = EngineeredChatgptPrompts()
    app.exec_()
