# PTE Practice Coach (Web)

A lightweight Flask web app to practice for the Pearson Test of English (PTE). It offers quick practice activities for speaking, writing, listening, and reading, all in your browser.

## Features
- **Speaking:** Built-in microphone capture with live speech-to-text transcript, rotating prompts, a 40-second timer, and note-taking space for describe-image or repeat-lecture style tasks.
- **Writing:** Rotating prompts for summarize-written-text and essay tasks, with instant word-count feedback, keyword coverage, and cohesion hints.
- **Listening:** Short lecture transcripts with summary prompts and keyword coverage checks to ensure your notes capture key points.
- **Reading:** Multiple-choice single-answer questions with explanations so you can review why the correct option works.

## Requirements
- Python 3.9+ with pip
- Recommended: create a virtual environment

## Setup and run
1) Install dependencies:

```bash
pip install -r requirements.txt
```

2) Start the web app:

```bash
python main.py
```

3) Open your browser to http://localhost:5000 and use the navigation bar to switch between sections.

Quick start from scratch:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\\Scripts\\activate
pip install -r requirements.txt
python main.py
```

Then visit http://localhost:5000 to begin on the Home page and choose a skill area.

## How to use each section
- **Speaking:** Read the prompt, press **Start voice capture** to allow mic access and see a live transcript of what you say. Stop capture when done, jot extra notes in the text box, and review fluency/pronunciation and content coverage. Use **Next prompt** to rotate topics and the built-in 40s timer to mirror test pacing.
- **Writing:** Type your response and click **Evaluate draft** to see word count, cohesion hints, and keyword coverage. Use **Next prompt** for another task.
- **Listening:** Read the short transcript once, answer the summary prompt in 1–2 sentences, then click **Evaluate summary**. Feedback shows word length and which target keywords you captured; **Next lecture** moves to another practice item.
- **Reading:** Choose the best option and press **Submit** to see if you’re correct and why. **Next question** loads the next item.

## Tips for use
- Speak for the full timer when recording yourself; prioritize clarity and natural pacing.
- Plan 1-2 minutes before writing so your structure is clear.
- For summaries, aim for 30-50 words and include the main nouns and verbs from the source.
- In reading tasks, skim the question before scanning the passage for evidence.

## Troubleshooting
- **Saw a Tkinter `unknown option "-wraplength"` error?** That comes from the earlier desktop prototype. This project now runs as a web app; launch it with `python main.py` and open http://localhost:5000 instead of using Tkinter. If you still want the desktop script, switch the radio buttons to `tk.Radiobutton` (they support `wraplength`) or remove that option.
