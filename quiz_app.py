import tkinter as tk
from tkinter import messagebox
import json
import os
import importlib

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PyPass Quiz App")

        # Initialize topics dynamically
        self.topics = {}
        self.load_topics()

        # Load previous scores (if any)
        self.load_scores()

        # Topic selection screen
        self.topic_label = tk.Label(self.root, text="Select a topic", font=("Arial", 18))
        self.topic_label.pack(pady=20)

        self.topic_button_frame = tk.Frame(self.root)
        self.topic_button_frame.pack()

        self.topic_buttons = {}
        for topic in self.topics:
            button = tk.Button(self.topic_button_frame, text=topic, font=("Arial", 14), width=20, command=lambda t=topic: self.start_quiz(t))
            button.pack(pady=5)
            self.topic_buttons[topic] = button

        # View scores button
        self.view_scores_button = tk.Button(self.root, text="View Previous Scores", font=("Arial", 14), command=self.view_scores)
        self.view_scores_button.pack(pady=10)

        self.score = 0
        self.current_question = 0
        self.total_questions = 0
        self.questions = []

    def load_topics(self):
        """ Load topics dynamically from the 'topics' folder. """
        topics_folder = "topics"
        for filename in os.listdir(topics_folder):
            if filename.endswith(".py"):
                topic_name = filename.replace(".py", "")
                module = importlib.import_module(f"topics.{topic_name}")
                self.topics[topic_name] = module.questions

    def load_scores(self):
        """ Load the previous scores from a file if it exists """
        if os.path.exists("scores.json"):
            with open("scores.json", "r") as file:
                self.scores = json.load(file)
        else:
            self.scores = {}

    def save_scores(self):
        """ Save the current score to a file """
        with open("scores.json", "w") as file:
            json.dump(self.scores, file)

    def start_quiz(self, topic):
        """ Start the quiz based on the selected topic """
        self.score = 0
        self.current_question = 0
        self.questions = self.topics[topic]
        self.total_questions = len(self.questions)

        # Hide the topic selection buttons
        self.topic_label.pack_forget()
        self.topic_button_frame.pack_forget()

        # Show quiz UI
        self.question_label = tk.Label(self.root, text=self.questions[self.current_question][0], font=("Arial", 18))
        self.question_label.pack(pady=10)

        self.answer_entry = tk.Entry(self.root, font=("Arial", 16))
        self.answer_entry.pack(pady=10)

        self.submit_button = tk.Button(self.root, text="Submit Answer", font=("Arial", 16), command=self.submit_answer)
        self.submit_button.pack(pady=20)

        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Arial", 16))
        self.score_label.pack(pady=10)

    def submit_answer(self):
        """ Check the user's answer and proceed to the next question """
        answer = self.answer_entry.get().strip()
        correct_answer = self.questions[self.current_question][1]

        if answer.lower() == correct_answer.lower():
            self.score += 1

        self.score_label.config(text=f"Score: {self.score}")

        self.current_question += 1
        if self.current_question < self.total_questions:
            self.question_label.config(text=self.questions[self.current_question][0])
            self.answer_entry.delete(0, tk.END)
        else:
            self.end_quiz()

    def end_quiz(self):
        """ End the quiz and save the score """
        topic = self.questions[0][0].split()[0]  # Assuming topic is part of question text (improve this part as needed)
        self.scores[topic] = self.score
        self.save_scores()
        messagebox.showinfo("Quiz Over", f"Your final score is: {self.score} out of {self.total_questions}")

        # Show 'Back to Main Menu' button
        self.show_back_button()

    def show_back_button(self):
        """ Show a button to go back to the main menu """
        self.back_button = tk.Button(self.root, text="Back to Main Menu", font=("Arial", 16), command=self.show_topic_selection)
        self.back_button.pack(pady=10)

    def show_topic_selection(self):
        """ Show the topic selection screen again """
        if hasattr(self, 'back_button'):
            self.back_button.pack_forget()
        
        self.question_label.pack_forget()
        self.answer_entry.pack_forget()
        self.submit_button.pack_forget()
        self.score_label.pack_forget()

        self.topic_label.pack(pady=20)
        self.topic_button_frame.pack()

    def view_scores(self):
        """ Display the user's previous scores """
        score_text = "Your Previous Scores:\n\n"
        for topic, score in self.scores.items():
            score_text += f"{topic}: {score}\n"
        
        # Show 'Back to Main Menu' button after viewing scores
        messagebox.showinfo("Previous Scores", score_text)
        self.show_back_button()
