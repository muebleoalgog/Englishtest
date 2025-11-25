import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class MultipleChoiceQuestion:
    prompt: str
    options: List[str]
    answer_index: int
    explanation: str


@dataclass
class WritingPrompt:
    title: str
    task: str
    tips: List[str]
    keywords: List[str] = field(default_factory=list)


@dataclass
class ListeningExercise:
    title: str
    transcript: str
    question: str
    keywords: List[str]


SPEAKING_PROMPTS = [
    "Describe a time when you had to solve a problem creatively.",
    "Explain a recent news story to a friend who has not heard it before.",
    "Summarize a book or movie you enjoyed and why you recommend it.",
    "Discuss the advantages and disadvantages of working from home.",
]


WRITING_PROMPTS = [
    WritingPrompt(
        title="Summarize Written Text",
        task=(
            "Read a short passage and write a one-sentence summary in under 75 words. "
            "Focus on the main idea, avoid examples, and connect clauses with linking words."
        ),
        tips=[
            "Capture who, what, where, and why in one sentence.",
            "Use connectors like 'because', 'which', or 'therefore' to join ideas.",
            "Aim for 40-55 words while keeping grammar simple.",
        ],
        keywords=["summary", "main", "idea"],
    ),
    WritingPrompt(
        title="Essay Writing",
        task=(
            "Write a 200-300 word persuasive essay on the topic. Structure with an introduction, "
            "two body paragraphs, and a conclusion."
        ),
        tips=[
            "Use a clear thesis statement in the introduction.",
            "Start each body paragraph with a controlling idea.",
            "Paraphrase the thesis when concluding and include a recommendation.",
        ],
        keywords=["introduction", "paragraph", "conclusion"],
    ),
]


LISTENING_EXERCISES = [
    ListeningExercise(
        title="Academic Lecture",
        transcript=(
            "Today we explored how urban green spaces moderate city temperatures. Parks absorb less heat, "
            "provide shade, and increase evaporation, creating a cooling effect known as urban greening."
        ),
        question="Summarize the lecture in 1-2 sentences focusing on the main idea.",
        keywords=["green", "cooling", "urban"],
    ),
    ListeningExercise(
        title="Business Briefing",
        transcript=(
            "The company will pilot a four-day workweek next quarter to boost productivity and employee satisfaction. "
            "Managers will monitor output and client feedback to decide whether to make the schedule permanent."
        ),
        question="Explain the goal of the pilot and how success will be measured.",
        keywords=["pilot", "productivity", "feedback"],
    ),
]


READING_QUESTIONS = [
    MultipleChoiceQuestion(
        prompt="Urban planners mention 'urban greening' primarily because it...",
        options=[
            "reduces noise from traffic.",
            "lowers city temperatures.",
            "increases apartment prices.",
            "limits recreational space.",
        ],
        answer_index=1,
        explanation="Urban greening cools cities through shade and evaporation, lowering temperatures.",
    ),
    MultipleChoiceQuestion(
        prompt="In the business briefing, success of the new schedule depends on...",
        options=[
            "higher product prices.",
            "employee satisfaction and client feedback.",
            "adding more weekly meetings.",
            "changing office locations.",
        ],
        answer_index=1,
        explanation="Managers will track productivity and client feedback before making the schedule permanent.",
    ),
]


def evaluate_keyword_coverage(text: str, keywords: List[str]) -> int:
    text_lower = text.lower()
    return sum(1 for kw in keywords if kw.lower() in text_lower)


def evaluate_writing(text: str, target_low: int = 200, target_high: int = 300) -> str:
    words = [w for w in text.split() if w.strip()]
    word_count = len(words)
    feedback = [f"Word count: {word_count} (aim for {target_low}-{target_high})."]

    if word_count < target_low:
        feedback.append("Add more development to meet the minimum length.")
    elif word_count > target_high:
        feedback.append("Trim unnecessary details to stay concise.")
    else:
        feedback.append("Great length for PTE expectations.")

    if any(word.istitle() for word in words[:5]):
        feedback.append("Strong start—your introduction looks clear.")
    else:
        feedback.append("Begin with a clear thesis statement in the first line.")

    connectors = {"because", "however", "therefore", "moreover", "although"}
    connector_hits = evaluate_keyword_coverage(text, list(connectors))
    if connector_hits < 2:
        feedback.append("Use more linking words to show cohesion (e.g., 'however', 'therefore').")
    else:
        feedback.append("Good cohesion with linking words.")

    return " \n".join(feedback)


class PTEPracticeApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("PTE Practice Coach")
        self.geometry("780x520")
        self.resizable(True, True)
        self.configure(padx=14, pady=12)

        self.section_var = tk.StringVar(value="Speaking")
        self.status_var = tk.StringVar(value="Select a task to begin practicing.")
        self.reading_index = 0
        self.writing_index = 0
        self.listening_index = 0

        self._build_header()
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill="both", expand=True, pady=10)

        self.status_bar = ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w")
        self.status_bar.pack(fill="x")

        self.render_speaking()

    def _build_header(self) -> None:
        header = ttk.Frame(self)
        header.pack(fill="x")

        ttk.Label(header, text="PTE English Skills", font=("Segoe UI", 16, "bold")).pack(side="left")

        section_choices = ["Speaking", "Writing", "Listening", "Reading"]
        ttk.Label(header, text="Practice area:", padding=(16, 0, 8, 0)).pack(side="left")

        section_box = ttk.Combobox(header, textvariable=self.section_var, values=section_choices, state="readonly")
        section_box.pack(side="left")
        section_box.bind("<<ComboboxSelected>>", self._on_section_change)

        ttk.Button(header, text="Quick tip", command=self._show_tip).pack(side="right")

    def _clear_content(self) -> None:
        for child in self.content_frame.winfo_children():
            child.destroy()

    def _on_section_change(self, event=None) -> None:  # type: ignore[override]
        section = self.section_var.get()
        if section == "Speaking":
            self.render_speaking()
        elif section == "Writing":
            self.render_writing()
        elif section == "Listening":
            self.render_listening()
        elif section == "Reading":
            self.render_reading()

    def _show_tip(self) -> None:
        tips = {
            "Speaking": "Speak for the full time and focus on clarity over speed.",
            "Writing": "Plan for 1-2 minutes so your structure is clear before typing.",
            "Listening": "Note key nouns and verbs—they carry most of the meaning.",
            "Reading": "Skim the question first, then scan the passage for evidence.",
        }
        messagebox.showinfo("Quick Tip", tips.get(self.section_var.get(), "Practice regularly!"))

    # Speaking
    def render_speaking(self) -> None:
        self._clear_content()
        prompt = SPEAKING_PROMPTS[0]
        ttk.Label(self.content_frame, text="Describe Image / Repeat Lecture", font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 6))
        ttk.Label(self.content_frame, text=prompt, wraplength=700, justify="left").pack(anchor="w", pady=(0, 12))

        ttk.Label(self.content_frame, text="Note-taking area:").pack(anchor="w")
        notes = tk.Text(self.content_frame, height=8, width=80)
        notes.pack(fill="both", expand=True)

        ttk.Label(
            self.content_frame,
            text=(
                "Record yourself with any voice recorder and compare against official PTE speaking criteria: "
                "fluency, pronunciation, and content coverage."
            ),
            wraplength=700,
            justify="left",
        ).pack(anchor="w", pady=10)

        self.status_var.set("Speaking: prepare briefly, then speak smoothly for the full timer.")

    # Writing
    def render_writing(self) -> None:
        self._clear_content()
        prompt = WRITING_PROMPTS[self.writing_index % len(WRITING_PROMPTS)]

        ttk.Label(self.content_frame, text=prompt.title, font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 6))
        ttk.Label(self.content_frame, text=prompt.task, wraplength=700, justify="left").pack(anchor="w", pady=(0, 6))

        tips_frame = ttk.LabelFrame(self.content_frame, text="Examiner reminders")
        tips_frame.pack(fill="x", pady=6)
        for tip in prompt.tips:
            ttk.Label(tips_frame, text=f"• {tip}", wraplength=680, justify="left").pack(anchor="w", padx=8, pady=2)

        self.writing_box = tk.Text(self.content_frame, height=10, width=90)
        self.writing_box.pack(fill="both", expand=True, pady=8)

        self.writing_feedback = ttk.Label(self.content_frame, text="Word count: 0", justify="left")
        self.writing_feedback.pack(anchor="w")

        controls = ttk.Frame(self.content_frame)
        controls.pack(anchor="e", pady=4)
        ttk.Button(controls, text="Evaluate draft", command=lambda: self._score_writing(prompt)).pack(side="left", padx=4)
        ttk.Button(controls, text="Next prompt", command=self._next_writing_prompt).pack(side="left", padx=4)

        self.status_var.set("Writing: aim for clear structure and concise sentences.")

    def _score_writing(self, prompt: WritingPrompt) -> None:
        text = self.writing_box.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("No text", "Please write your response before evaluating.")
            return

        feedback_lines = [evaluate_writing(text)]
        keyword_hits = evaluate_keyword_coverage(text, prompt.keywords)
        feedback_lines.append(f"Keyword coverage: {keyword_hits}/{len(prompt.keywords)} core ideas mentioned.")

        self.writing_feedback.config(text="\n".join(feedback_lines))
        self.status_var.set("Writing feedback updated. Adjust your draft based on the notes.")

    def _next_writing_prompt(self) -> None:
        self.writing_index += 1
        self.render_writing()

    # Listening
    def render_listening(self) -> None:
        self._clear_content()
        exercise = LISTENING_EXERCISES[self.listening_index % len(LISTENING_EXERCISES)]

        ttk.Label(self.content_frame, text=exercise.title, font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 6))
        ttk.Label(self.content_frame, text="Transcript (read once, then hide it in the real test)", font=("Segoe UI", 9, "italic")).pack(anchor="w")

        transcript_box = tk.Text(self.content_frame, height=6, wrap="word", state="normal")
        transcript_box.insert("1.0", exercise.transcript)
        transcript_box.config(state="disabled")
        transcript_box.pack(fill="both", expand=False, pady=6)

        ttk.Label(self.content_frame, text=exercise.question, wraplength=700, justify="left").pack(anchor="w", pady=(0, 6))

        self.listening_box = tk.Text(self.content_frame, height=8, width=90)
        self.listening_box.pack(fill="both", expand=True)

        self.listening_feedback = ttk.Label(self.content_frame, text="Write a 1-2 sentence summary.")
        self.listening_feedback.pack(anchor="w", pady=4)

        controls = ttk.Frame(self.content_frame)
        controls.pack(anchor="e", pady=4)
        ttk.Button(controls, text="Evaluate summary", command=lambda: self._score_listening(exercise)).pack(side="left", padx=4)
        ttk.Button(controls, text="Next lecture", command=self._next_listening_exercise).pack(side="left", padx=4)

        self.status_var.set("Listening: capture nouns/verbs and link them with transition words.")

    def _score_listening(self, exercise: ListeningExercise) -> None:
        text = self.listening_box.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("No summary", "Write a short summary before evaluating.")
            return

        words = len(text.split())
        coverage = evaluate_keyword_coverage(text, exercise.keywords)
        feedback = [f"Length: {words} words (aim for 30-50).", f"Keyword coverage: {coverage}/{len(exercise.keywords)}."]
        if coverage == len(exercise.keywords):
            feedback.append("Great! You captured the main points.")
        else:
            missing = [kw for kw in exercise.keywords if kw.lower() not in text.lower()]
            feedback.append("Add details about: " + ", ".join(missing))

        self.listening_feedback.config(text="\n".join(feedback))
        self.status_var.set("Listening feedback updated. Refine your summary.")

    def _next_listening_exercise(self) -> None:
        self.listening_index += 1
        self.render_listening()

    # Reading
    def render_reading(self) -> None:
        self._clear_content()
        question = READING_QUESTIONS[self.reading_index % len(READING_QUESTIONS)]

        ttk.Label(self.content_frame, text="Multiple-choice, single answer", font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 6))
        ttk.Label(self.content_frame, text=question.prompt, wraplength=700, justify="left").pack(anchor="w", pady=(0, 8))

        self.reading_choice = tk.IntVar(value=-1)
        for idx, option in enumerate(question.options):
            ttk.Radiobutton(self.content_frame, text=option, variable=self.reading_choice, value=idx, wraplength=680).pack(anchor="w", pady=2)

        self.reading_feedback = ttk.Label(self.content_frame, text="Select the best answer and submit.")
        self.reading_feedback.pack(anchor="w", pady=6)

        controls = ttk.Frame(self.content_frame)
        controls.pack(anchor="e", pady=4)
        ttk.Button(controls, text="Submit", command=lambda: self._score_reading(question)).pack(side="left", padx=4)
        ttk.Button(controls, text="Next question", command=self._next_reading_question).pack(side="left", padx=4)

        self.status_var.set("Reading: pick the option that directly answers the question.")

    def _score_reading(self, question: MultipleChoiceQuestion) -> None:
        choice = self.reading_choice.get()
        if choice == -1:
            messagebox.showwarning("No option selected", "Please choose an answer before submitting.")
            return

        if choice == question.answer_index:
            feedback = "Correct! " + question.explanation
        else:
            feedback = f"Not quite. {question.explanation}"

        self.reading_feedback.config(text=feedback)
        self.status_var.set("Reading feedback updated. Move to the next question to keep practicing.")

    def _next_reading_question(self) -> None:
        self.reading_index += 1
        self.render_reading()


def main() -> None:
    app = PTEPracticeApp()
    app.mainloop()


if __name__ == "__main__":
    main()
