# main.py
# Main entry point for the quiz application
# Uses Tkinter for GUI

import tkinter as tk
from tkinter import messagebox
import random
from questions import questions

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")
        self.root.geometry("750x550")
        self.root.resizable(False, False)

        # Shuffle questions for randomization
        self.questions = questions.copy()
        random.shuffle(self.questions)

        self.current_question = 0
        self.score = 0
        title = tk.Label(root, text="Python Quiz App", font=("Arial", 24, "bold"))
        title.pack(pady=10)

        # UI Elements
        self.question_label = tk.Label(root, text="", font=("Arial", 18), wraplength=500, justify="center")
        self.question_label.pack(pady=20)

        self.progress_label = tk.Label(root, text="", font=("Arial", 10))
        self.progress_label.pack(pady=5)

        self.options_frame = tk.Frame(root)
        self.options_frame.pack(pady=20)

        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(self.options_frame, text="", font=("Arial", 12), width=30, command=lambda idx=i: self.check_answer(idx))
            btn.pack(pady=5)
            self.option_buttons.append(btn)

        self.next_button = tk.Button(root, text="Next", font=("Arial", 12), command=self.next_question, state=tk.DISABLED)
        self.next_button.pack(pady=10)

        self.load_question()

    def load_question(self):
        if self.current_question < len(self.questions):
            q = self.questions[self.current_question]
            self.question_label.config(text=q["question"])
            self.progress_label.config(text=f"Question {self.current_question + 1} of {len(self.questions)}")
            for i, option in enumerate(q["options"]):
                self.option_buttons[i].config(text=option, state=tk.NORMAL, bg="SystemButtonFace")
            self.next_button.config(state=tk.DISABLED)
        else:
            self.show_results()

    def check_answer(self, idx):
        q = self.questions[self.current_question]
        selected = q["options"][idx]
        if selected == q["answer"]:
            self.score += 1
            self.option_buttons[idx].config(bg="green")
        else:
            self.option_buttons[idx].config(bg="red")
            # Highlight correct answer
            for i, opt in enumerate(q["options"]):
                if opt == q["answer"]:
                    self.option_buttons[i].config(bg="green")
                    break
        # Disable all buttons
        for btn in self.option_buttons:
            btn.config(state=tk.DISABLED)
        self.next_button.config(state=tk.NORMAL)

    def next_question(self):
        self.current_question += 1
        self.load_question()

    def show_results(self):
    # Hide question elements
      self.question_label.pack_forget()
      self.progress_label.pack_forget()
      self.options_frame.pack_forget()
      self.next_button.pack_forget()

    # Calculate percentage
      percentage = (self.score / len(self.questions)) * 100

    # Show results
      result_label = tk.Label(
        self.root,
        text=f"Your Score: {self.score}/{len(self.questions)}\nPercentage: {percentage:.0f}%",
        font=("Arial", 16)
    )
      result_label.pack(pady=20)

      retry_button = tk.Button(self.root, text="Retry", font=("Arial", 12), command=self.retry_quiz)
      retry_button.pack(pady=10)

      exit_button = tk.Button(self.root, text="Exit", font=("Arial", 12), command=self.root.quit)
      exit_button.pack(pady=10)

    def retry_quiz(self):
        # Reset
        self.current_question = 0
        self.score = 0
        random.shuffle(self.questions)
        # Show elements again
        self.question_label.pack(pady=20)
        self.progress_label.pack(pady=5)
        self.options_frame.pack(pady=20)
        self.next_button.pack(pady=10)
        # Remove result elements
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label) and widget != self.question_label and widget != self.progress_label:
                widget.destroy()
            elif isinstance(widget, tk.Button) and widget not in self.option_buttons and widget != self.next_button:
                widget.destroy()
        self.load_question()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
