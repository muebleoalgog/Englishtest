# PTE Practice Coach (Web)

A lightweight Flask web app to practice for the Pearson Test of English (PTE). It offers quick practice activities for speaking, writing, listening, and reading, all in your browser.

## Features
- **Speaking:** Note-taking space and guidance for recording your own responses to describe-image or repeat-lecture style tasks.
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

## How to use each section
- **Speaking:** Read the prompt, jot notes in the text box, then record yourself with any voice recorder app. Listen back and check fluency, pronunciation, and whether you covered the key ideas.
- **Writing:** Type your response and click **Evaluate draft** to see word count, cohesion hints, and keyword coverage. Use **Next prompt** for another task.
- **Listening:** Read the short transcript once, answer the summary prompt in 1–2 sentences, then click **Evaluate summary**. Feedback shows word length and which target keywords you captured; **Next lecture** moves to another practice item.
- **Reading:** Choose the best option and press **Submit** to see if you’re correct and why. **Next question** loads the next item.

## Tips for use
- Speak for the full timer when recording yourself; prioritize clarity and natural pacing.
- Plan 1-2 minutes before writing so your structure is clear.
- For summaries, aim for 30-50 words and include the main nouns and verbs from the source.
- In reading tasks, skim the question before scanning the passage for evidence.
