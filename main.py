from dataclasses import dataclass, field
from typing import List, Dict

from flask import Flask, render_template, request


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


QUICK_TIPS: Dict[str, str] = {
    "speaking": "Speak for the full time and focus on clarity over speed.",
    "writing": "Plan for 1-2 minutes so your structure is clear before typing.",
    "listening": "Note key nouns and verbs—they carry most of the meaning.",
    "reading": "Skim the question first, then scan the passage for evidence.",
}


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

    return "<br>".join(feedback)


def evaluate_listening_summary(text: str, exercise: ListeningExercise) -> str:
    if not text:
        return "Write a short summary before evaluating."

    words = len(text.split())
    coverage = evaluate_keyword_coverage(text, exercise.keywords)
    feedback = [f"Length: {words} words (aim for 30-50).", f"Keyword coverage: {coverage}/{len(exercise.keywords)}."]
    if coverage == len(exercise.keywords):
        feedback.append("Great! You captured the main points.")
    else:
        missing = [kw for kw in exercise.keywords if kw.lower() not in text.lower()]
        feedback.append("Add details about: " + ", ".join(missing))
    return "<br>".join(feedback)


def evaluate_reading_answer(choice: int, question: MultipleChoiceQuestion) -> str:
    if choice == question.answer_index:
        return "Correct! " + question.explanation
    return "Not quite. " + question.explanation


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/")
    def home():
        return render_template("home.html", active="home", quick_tip="Practice regularly!")

    @app.route("/speaking")
    def speaking():
        prompt = SPEAKING_PROMPTS[0]
        return render_template(
            "speaking.html",
            prompt=prompt,
            active="speaking",
            quick_tip=QUICK_TIPS["speaking"],
        )

    @app.route("/writing", methods=["GET", "POST"])
    def writing():
        prompt_index = int(request.args.get("prompt", 0)) % len(WRITING_PROMPTS)
        prompt = WRITING_PROMPTS[prompt_index]
        response = request.form.get("response", "") if request.method == "POST" else ""
        feedback = ""
        if request.method == "POST" and response.strip():
            keyword_hits = evaluate_keyword_coverage(response, prompt.keywords)
            feedback_lines = [evaluate_writing(response)]
            feedback_lines.append(
                f"Keyword coverage: {keyword_hits}/{len(prompt.keywords)} core ideas mentioned."
            )
            feedback = "<br>".join(feedback_lines)
        elif request.method == "POST":
            feedback = "Please write your response before evaluating."

        next_index = (prompt_index + 1) % len(WRITING_PROMPTS)
        return render_template(
            "writing.html",
            prompt=prompt,
            next_index=next_index,
            feedback=feedback,
            response=response,
            active="writing",
            quick_tip=QUICK_TIPS["writing"],
        )

    @app.route("/listening", methods=["GET", "POST"])
    def listening():
        exercise_index = int(request.args.get("exercise", 0)) % len(LISTENING_EXERCISES)
        exercise = LISTENING_EXERCISES[exercise_index]
        summary = request.form.get("summary", "") if request.method == "POST" else ""
        feedback = ""
        if request.method == "POST":
            feedback = evaluate_listening_summary(summary.strip(), exercise)

        next_index = (exercise_index + 1) % len(LISTENING_EXERCISES)
        return render_template(
            "listening.html",
            exercise=exercise,
            next_index=next_index,
            feedback=feedback,
            summary=summary,
            active="listening",
            quick_tip=QUICK_TIPS["listening"],
        )

    @app.route("/reading", methods=["GET", "POST"])
    def reading():
        question_index = int(request.args.get("question", 0)) % len(READING_QUESTIONS)
        question = READING_QUESTIONS[question_index]
        feedback = ""
        selected = None
        if request.method == "POST":
            choice_raw = request.form.get("choice")
            if choice_raw is not None:
                selected = int(choice_raw)
                feedback = evaluate_reading_answer(selected, question)
            else:
                feedback = "Please select an answer before submitting."

        next_index = (question_index + 1) % len(READING_QUESTIONS)
        return render_template(
            "reading.html",
            question=question,
            next_index=next_index,
            feedback=feedback,
            selected=selected,
            active="reading",
            quick_tip=QUICK_TIPS["reading"],
        )

    return app


def main() -> None:
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=False)


if __name__ == "__main__":
    main()
