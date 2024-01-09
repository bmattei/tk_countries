from tkinter import *
from tkinter import Frame
from tkinter import ttk


from backend.questions import Questions


class QuizController:
    msg_frame: Frame
    levels = ["Beginner", "Advanced", "Expert"]

    def __init__(self):
        self.correct = 0
        self.incorrect = 0
        self.root = Tk()
        self.root.title("Quiz Game")
        self.root.geometry("600x400")
        self.msg_frame = ttk.Frame(self.root,  borderwidth=5)
        self.msg_frame.pack()
        msg = ttk.Label(self.msg_frame, text="Let's get started!")
        msg.pack()
        self.game_frame = ttk.Frame(self.root)
        self.game_frame.pack()
        self.questions = NONE
        self.current_qa = NONE

    def create_level_screen(self):
        level_label = ttk.Label(self.game_frame, text="What level of difficulty?")
        level_label.pack()
        for level in QuizController.levels:
            button = ttk.Button(self.game_frame, text=level,
                            command=lambda label=level: self.set_level(label))
            button.pack()

    def set_level(self, level):
        self.clear(self.msg_frame)
        self.clear(self.game_frame)
        self.questions = Questions(level)
        self.ask_question()

    def clear(self, top_widget):
        for widget in top_widget.winfo_children():
            widget.destroy()

    def end_quiz(self):
        self.clear(self.msg_frame)
        self.clear(self.game_frame)
        total = self.correct + self.incorrect
        if total > 0:
            percentage_str = f"{round(self.correct / total * 100,2)}%"
            final_result = ttk.Label(self.msg_frame,
                                text=f"{percentage_str} {self.correct} out of {total}")
            final_result.pack()
        else:
            msg = ttk.Label(self.msg_frame, text="   Sorry to see you go!  ")

    def ask_question(self):
        msg = ttk.Label(self.msg_frame,
                    text=f"correct: {self.correct} incorrect: {self.incorrect}")
        msg.pack()
        qa = self.questions.get_question()
        if not bool(qa):
            self.end_quiz()
        else:
            self.current_qa = qa
            q_label = ttk.Label(self.game_frame, text=qa["Question"])
            q_label.pack()
            choice: object
            for choice in qa["Choices"]:
                button = ttk.Button(self.game_frame, text=choice, command=lambda label=choice: self.answer_click(label))
                button.pack()
            exit_button = ttk.Button(self.game_frame, text="exit",
                             command=self.end_quiz)

            exit_button.pack()

    def answer_click(self, label):
        if label == self.current_qa["Answer"]:
            self.correct += 1
        else:
            self.incorrect += 1
        self.clear(self.msg_frame)

        self.clear(self.game_frame)
        self.ask_question()


    def start_quiz(self):
        self.create_level_screen()
        self.root.mainloop()


if __name__ == "__main__":
    controller = QuizController()
    controller.start_quiz()
