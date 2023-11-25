"""
This is a simple PyQt5 GUI application that allows to create elaborated
chatgtp prompts. Using a specified goal, the input text is processed
by the chatgpt model to generate the output text.
"""

# import asyncio
import openai
import os
from dotenv import load_dotenv, find_dotenv
from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QVBoxLayout,
                             QHBoxLayout,
                             QLabel,
                             QFileDialog,
                             QTextEdit,
                             QPushButton)

_ = load_dotenv(find_dotenv())  # read local .env file

# TODO: use async client
#client = openai.AsyncOpenAI(
#    api_key=os.getenv('OPENAI_API_KEY'),
#    organization=os.getenv('OPENAI_ORGANIZATION'),
#)

openai.organization = os.getenv('OPENAI_ORGANIZATION')
openai.api_key = os.getenv('OPENAI_API_KEY')


async def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    chat = None
    try:
        # chat = await client.chat.completions.create(
        chat = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0,
            # this is the randomness degree of the model's output
        )
    except openai.error.InvalidRequestError as err:
        print(f"InvalidRequestError: {err}")
        return None

    if chat is None:
        print(f"Invalid Response")
        return None
    return chat.choices[0].message["content"]


class EngineeredChatgptPrompts(QWidget):
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
        input = self.input_text.toPlainText()
        goal = self.goal_text.toPlainText()
        # Perform processing on the input text (replace with your own logic)
        if len(goal) < 2:
            goal = "summarize in 2 sentence"
        complete_prompt = (f"with the following goal "
                           f"(delimited by triple backticks): ```{goal}```"
                           f"process the following text with specified goal"
                           f"(delimited by triple backticks): ```{input}```")
        processed_text = get_completion(complete_prompt)
        processed_text = f'Processed Text:\n{processed_text}'
        self.output_text.setText(processed_text)

    def load_goal(self):
        # open a dialog inspecting text files on current folder
        filename = QFileDialog.getOpenFileName(self,
                                               'Open File',
                                               '.',
                                               'Text Files (*.txt)')
        if filename[0]:
            with open(filename[0], 'r') as f:
                file_text = f.read()
                self.goal_text.setText(file_text)

    def save_goal(self):
        filename = QFileDialog.getSaveFileName(self,
                                               'Save File',
                                               '.',
                                               'Text Files (*.txt)')
        if filename[0]:
            with open(filename[0], 'w') as f:
                my_text = self.goal_text.toPlainText()
                f.write(my_text)

    def clear_goal(self):
        self.goal_text.setText('')

    def clear_input(self):
        self.input_text.setText('')


if __name__ == '__main__':
    app = QApplication([])
    window = EngineeredChatgptPrompts()
    app.exec_()
