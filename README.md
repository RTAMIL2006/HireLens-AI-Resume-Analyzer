<<<<<<< HEAD
# AI Resume–Job Match Analyzer

A Python + NLP web application that analyzes how well a resume matches a
job description, producing a transparent, explainable **Resume–Job Match
Score**, detailed skill/keyword gap analysis, resume structure feedback,
bullet-point quality review, and honest, non-fabricated recommendations.

## Overview

Most online "resume checkers" are black boxes: you get a number with no
idea how it was produced. This project takes the opposite approach —
**every score, match, and recommendation is derived from a method you can
explain line-by-line**, using free, open-source NLP and machine learning
techniques (spaCy, TF-IDF, cosine similarity, regex). It was built to be
genuinely understandable and defensible in a technical interview, not
just impressive-looking.

> **This is a Resume–Job Match Score, not a guaranteed ATS score.** Real
> Applicant Tracking Systems are proprietary and vary company to company.
> This tool is an independent, open, and explainable estimate to help you
> improve your resume — it does not claim to reproduce any company's
> actual ATS.

## Problem Statement

Job seekers often don't know *why* their resume isn't landing interviews,
and generic advice ("use more keywords!") isn't actionable. This project
gives a candidate a structured, honest breakdown of how their resume
compares to a specific job description — what's matched, what's missing,
how complete the resume's structure is, and concrete (never fabricated)
suggestions for improvement.

## Features

- Upload a resume as a **PDF** and extract its text (PyMuPDF)
- Paste any job description as plain text
- Text preprocessing pipeline (regex cleaning + spaCy tokenization,
  stopword removal, lemmatization)
- **Skill extraction** using a curated skill database with alias matching
  (e.g. "JS", "Javascript", "ReactJS" are all recognized as one skill)
- Matched / missing / additional skill detection, with **skill-gap
  priority** (High / Medium / Low, based on how often a missing skill is
  mentioned in the JD)
- **TF-IDF + Cosine Similarity** semantic matching between resume and JD
- **Resume section detection** (Summary, Education, Skills, Projects,
  Experience, Internships, Certifications, Achievements) with support for
  common alternative headings
- **Resume completeness score**, based on which expected sections are present
- **Keyword gap analysis** using spaCy POS tagging to find the JD's most
  frequent important terms, filtered to exclude generic job-posting
  boilerplate
- **Project/Experience/Internship relevance scoring**, including which
  specific project is most relevant to a given job description
- **Resume bullet-point analyzer**: checks for strong action verbs, weak
  passive phrases, mentioned technologies, and quantified results
- **Actionable recommendations** (Issue / Why it matters / Suggestion),
  generated only from real findings — never fabricated
- A transparent, 5-component weighted **Resume–Job Match Score (0–100)**
  with a full breakdown of exactly how it was calculated
- **Multi-job-description comparison** — see which of several roles your
  resume currently aligns with most strongly
- A clean, professional, light-themed Streamlit dashboard

## Demo / Screenshots

Run the app locally with `streamlit run app.py` (see
[Installation](#installation) below) to see the live dashboard — the gauge
score, skill chips, section badges, bullet-by-bullet review, and
recommendation cards.

## How It Works

1. **Extract** resume text from the uploaded PDF (PyMuPDF).
2. **Preprocess** both resume and JD text: regex cleaning, then spaCy
   tokenization, stopword removal, and lemmatization.
3. **Detect skills** in both documents using alias-based regex matching
   against a curated skill database — never a guess, only genuine text matches.
4. **Detect resume sections** by scanning line-by-line for known heading
   phrasings, and slice out each section's content.
5. **Score five signals independently**: skill match %, TF-IDF cosine
   similarity, keyword coverage %, resume completeness %, and
   project/experience relevance %.
6. **Combine** those five signals into one weighted, fully-disclosed final score.
7. **Analyze bullet points** for action verbs, weak phrasing, mentioned
   tech, and quantified results.
8. **Generate recommendations** purely from the findings above — no
   invented skills, achievements, or numbers.

## Architecture

```
User (Streamlit UI)
        │
        ▼
   app.py  ──────────────► orchestrates the pipeline, renders results
        │
        ▼
 ┌──────────────────────────── src/ ────────────────────────────┐
 │ pdf_extractor      → PDF → raw text                           │
 │ preprocessor       → cleaning, spaCy tokenizing/lemmatizing   │
 │ skills_data        → curated skill + alias database           │
 │ skill_extractor    → regex/alias skill detection & comparison │
 │ sections_data      → resume section heading aliases + weights │
 │ section_detector   → line-based resume section detection     │
 │ completeness       → weighted resume completeness score       │
 │ keyword_analyzer   → spaCy POS-based JD keyword extraction    │
 │ matcher            → TF-IDF + cosine similarity                │
 │ relevance          → project/experience relevance scoring     │
 │ bullet_analyzer    → bullet-point quality analysis             │
 │ recommendations    → turns findings into honest advice        │
 │ scorer             → combines 5 signals into final score      │
 └────────────────────────────────────────────────────────────────┘
```

Each module has one clear responsibility and no circular dependencies,
so it's easy to test, read, and explain piece by piece.

## Tech Stack

| Purpose | Technology |
|---|---|
| UI / Dashboard | Streamlit |
| PDF text extraction | PyMuPDF (`fitz`) |
| NLP (tokenizing, lemmatizing, POS tagging, stopwords) | spaCy |
| Similarity scoring | scikit-learn (TF-IDF + Cosine Similarity) |
| Text cleaning | Regex (`re`) |
| Tabular data display | Pandas |
| Visualization | Plotly |
| Testing | pytest |

No paid APIs, no external services — everything runs locally.

## NLP Techniques

- **Tokenization & Lemmatization** (spaCy): reduces words to base forms
  ("developing" → "develop") so similar phrasing matches consistently.
- **Stopword removal**: filters out common words ("the", "and", "is")
  that add noise to similarity comparisons.
- **Part-of-speech (POS) tagging**: used in keyword gap analysis to keep
  only nouns/proper nouns, which tend to carry the most topical meaning
  in a job description.
- **TF-IDF (Term Frequency–Inverse Document Frequency)**: represents each
  document as a vector of weighted word importances.
- **Cosine Similarity**: measures the angle between two TF-IDF vectors —
  a smaller angle means more shared, weighted vocabulary.
- **Regex-based alias matching**: matches known skill/section names and
  their common variants using word-boundary-safe regular expressions.

## Match Score Methodology

The **Resume–Job Match Score** is a weighted average of five signals:

| Signal | What it measures | Weight |
|---|---|---|
| Skill Match | % of JD's required skills found in the resume | 40% |
| Semantic Similarity | TF-IDF + cosine similarity between full resume & JD text | 25% |
| Keyword Coverage | % of the JD's most frequent important terms found in the resume | 15% |
| Resume Completeness | % of expected resume sections present | 10% |
| Project/Experience Relevance | Similarity of Projects/Experience/Internships to the JD | 10% |

```
Final Score = (Skill Match × 0.40) + (Semantic Similarity × 0.25)
            + (Keyword Coverage × 0.15) + (Completeness × 0.10)
            + (Relevance × 0.10)
```

Every raw sub-score, weight, and contribution is shown to the user in the
"How was this score calculated?" panel — nothing is hidden. Skill overlap
and semantic similarity carry the most weight since they most directly
reflect job fit; structural/quality signals (completeness, relevance)
are weighted lower.

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/resume-job-match-analyzer.git
   cd resume-job-match-analyzer
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download the spaCy English language model** (one-time step)
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Running Locally

```bash
streamlit run app.py
```

Streamlit opens the app automatically at `http://localhost:8501`. The app
always launches in **light theme** by default (`.streamlit/config.toml`).

## Project Structure

```
resume_analyzer/
├── app.py                        # Streamlit UI - orchestrates the pipeline
├── .streamlit/
│   └── config.toml               # Forces light theme as the default
├── src/
│   ├── __init__.py
│   ├── pdf_extractor.py          # PDF -> raw text (PyMuPDF)
│   ├── preprocessor.py           # Text cleaning + spaCy NLP pipeline
│   ├── skills_data.py            # Skill database + alias mappings
│   ├── skill_extractor.py        # Regex/alias-based skill detection & comparison
│   ├── sections_data.py          # Resume section heading aliases + weights
│   ├── section_detector.py       # Line-based resume section detection
│   ├── completeness.py           # Weighted resume completeness score
│   ├── keyword_analyzer.py       # spaCy POS-based JD keyword extraction
│   ├── matcher.py                # TF-IDF + cosine similarity
│   ├── relevance.py               # Project/experience relevance scoring
│   ├── bullet_analyzer.py        # Bullet-point quality analysis
│   ├── recommendations.py        # Turns findings into honest advice
│   └── scorer.py                 # Weighted final score + explanation
├── tests/                        # One test file per src/ module
├── sample_data/                  # (optional) local sample resumes for testing
├── requirements.txt
├── .gitignore
└── README.md
```

## Testing

```bash
pytest tests/ -v
```

The suite includes 68 tests covering every module in `src/` — PDF
extraction (including corrupted/scanned-PDF edge cases), preprocessing,
skill extraction and aliases, section detection (including alternative
headings), completeness scoring, keyword gap analysis, TF-IDF/cosine
similarity, project/experience relevance, bullet analysis, recommendation
generation, and the final weighted scorer. All tests generate their own
in-memory sample data (e.g. PDFs built on-the-fly with PyMuPDF) — no
external files are required to run the suite.

## Privacy

Your resume is processed only in memory for the duration of your
session. It is not uploaded to any third-party server, stored in a
database, or persisted anywhere after your session ends. The app does
not log resume text, emails, phone numbers, or any other personal
information.

## Limitations

- This is **not** a real ATS and makes no claim to replicate one.
- Skill extraction is alias/keyword-based, not a trained ML classifier —
  intentional, for full transparency and explainability.
- Section detection relies on recognizable heading text; unusual or
  highly stylized resume formats may not be detected correctly.
- Semantic similarity (TF-IDF + cosine) is sensitive to document length
  and exact vocabulary — a short, relevant bullet point can sometimes
  score lower than a longer, more verbose one that happens to reuse more
  of the JD's exact wording.
- The app never fabricates skills, experience, achievements, or scores.
  Every matched skill and every score component is derived directly and
  traceably from the text you provide.
- Keyword and skill matching works best with common, well-known tech
  terms (see `src/skills_data.py`) — very niche or misspelled terms may
  not be recognized.

## Future Improvements

- Support for DOCX resume uploads (not just PDF)
- Configurable weights (let the user adjust signal importance)
- Export the full analysis as a downloadable PDF/DOCX report
- Broader skill database covering more domains beyond software engineering
- Optional dark mode toggle (light mode remains the default)

## Author

Built as a final-year engineering student portfolio project to
demonstrate practical, explainable NLP, text processing, data analysis,
and full-stack Python application development — designed to be presented
and defended in technical interviews, not just displayed on GitHub.
=======

>>>>>>> 4a12478b61f0bdc49023bd2ac97f5b993e97dba8
