# Resume Intelligence Engine

### AI-powered Resume Ranking from PDFs using Python & LLMs

Resume Intelligence Engine is a Python tool that analyzes and ranks resumes (PDFs) using a Large Language Model. Users simply place their resume files inside the `resumes/` folder, adjust ranking parameters in the script (experience vs education weighting, required skills, minimum years of experience), and let the system score each candidate from **1 to 10** and return ranked results.

---

## ✨ Features

✔ **Drop-in PDF resumes** — place files inside the `resumes/` folder  
✔ **LLM-powered resume analysis**  
✔ **Customizable ranking parameters**  
✔ **Scoring system (1–10) with explanation**  
✔ **Sorted output of candidates**  
✔ **Uses Cloudflare AI HTTP API for LLM inference**  
✔ **Optional result export (CSV/JSON)**

---

## 📁 Project Structure

```
resume-intelligence-engine/
│
├── resumes/ # Place your PDF resumes here
├── results/ # Output scores & rankings
├── app.py # Main script
├── pdf_parser.py # Extract & clean PDF text
├── llm_backend.py # Local or API LLM interface
├── ranking_logic.py # Weighting, scoring, sorting
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/anastasios-b/resume-intelligence-engine.git
cd resume-intelligence-engine
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Cloudflare AI

This project now uses **Cloudflare AI** instead of a local Ollama installation.

Configure your Cloudflare credentials in `constants.py`:

```python
# constants.py
CLOUDFLARE_API_TOKEN = "your_api_token_here"
CLOUDFLARE_ACCOUNT_ID = "your_account_id_here"
# Optional: override default model (@cf/meta/llama-3-8b-instruct)
CLOUDFLARE_MODEL = "@cf/meta/llama-3-8b-instruct"
```

The underlying call is equivalent to the following `curl` request:

```bash
curl \
  https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/ai/run/@cf/meta/llama-3-8b-instruct \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Where did the phrase Hello World come from"}'
```

## 🛠️ Usage

### Step 1 — Add resumes

You can either:

- Manually place your own PDF resumes inside:

  ```
  resumes/
  ```

- Or generate realistic sample resumes using the helper script:

  ```bash
  python generate_sample_resumes.py
  ```

  This will create several software-engineering resumes in the `resumes/` folder.

### Step 2 — Adjust ranking parameters

Inside `app.py` you can configure:

```python
# Fields used to evaluate the candidates
TARGET_FIELD = "software engineering"

# IMPORTANT: The total sum of these indices must be 1
WEIGHT_EXPERIENCE = 0.5
WEIGHT_EDUCATION = 0.2
WEIGHT_GENERAL_SKILLS = 0.3

REQUIRED_QUALITIES = {
    # Required education
    "education": {
        "school": "high school diploma",
        "computer science": "bachelor degree",

        # Language and required level
        "languages": {
            "english": "conversational",
            "greek": "conversational",
        }
    },

    # Required core technical skills and minimum years of experience.
    # Each skill maps to an object with:
    #   - "years": minimum years required (int)
    #   - "relative_skills_accepted": bool
    #       * If True, related or nearby skills (synonyms, frameworks, or adjacent technologies)
    #         may be accepted to satisfy the requirement (e.g., 'Django' or 'Flask' for 'python').
    #       * If False, the candidate must explicitly list the exact skill.
    # Matching/scoring recommendations (implementation notes):
    #   - Treat 'years' as a minimum; compute a normalized score such as
    #       min(candidate_years / required_years, 1.0) for this skill.
    #   - If 'relative_skills_accepted' is True, allow partial credit for related skills
    #     (e.g., 0.5–0.9 depending on closeness) rather than binary pass/fail.
    #   - Consider establishing a small taxonomy or synonyms list for reliable matching.
    "specific_skills_and_experience_in_years": {
        "python": {
            "years": 2,
            "relative_skills_accepted": True, # E.g. PHP is accepted too
        },
        "aws": {
            "years": 2,
            "relative_skills_accepted": False, # Here, the candidate must have this exact skill
        },
        "machine learning": {
            "years": 2,
            "relative_skills_accepted": True, # E.g. LLM knowledge is accepted too
        },
    },

    # General skills, like ease of talking to clients, cooperation etc.
    "general_skills": [
        "contacting clients",
        "team work",
        "adaptability to new technologies"
    ],

    # Required acceptance of the following types of work
    "available_types_of_work": [
        "remote",
        "hybrid"
    ],

    # Required personal information (place of residence etc.)
    "personal_information": {
        "country": "Greece", # Candidate must live in this country
        "location": "Thessaloniki", # Candidate must live in this country
    }
}

# Good-to-have qualities, but not required.
# Candidates who cover the required ones and these too will rank higher than others.
# Uses the same fields as required qualities.
# Complete only the necessary.
OPTIONAL_QUALITIES = {
    "education": {
        "languages": {
            "german": "conversational"
        }
    },

    "specific_skills_and_experience_in_years": {
        "nodejs": {
            "years": 1,
            "relative_skills_accepted": False,
        }
    }
}
```

### Step 3 — Run the tool

```bash
python app.py
```

📊 Output Example

```markdown
Ranking completed!

1. John Smith — Score: 9.1/10
   Strong Python background, 4 years ML experience, relevant MSc.

2. Maria Papadopoulou — Score: 8.3/10
   Solid experience, moderate alignment with target field.

3. Alex Doe — Score: 6.7/10
   Missing required skills.
```

Details are saved in the `results/` folder.

## 🧠 How It Works

#### 1. PDF Parsing (Binary Mode):

The tool parses resumes in **binary format**, preserving the PDF's original content (layout, images, tables, etc.). No conversion to plain text is done at this stage—this ensures that the resume is passed to the LLM in its most understandable form.

#### 2. LLM Evaluation:

The **LLM** (whether local or API-based) processes the PDF's binary data, analyzing the content based on the user-defined criteria, such as experience vs. education, specific skills, and years of experience.

#### 3. Weighted Scoring:

Based on the LLM's evaluation and the weighting parameters (experience vs. education, required skills), the tool computes a final score for each resume, ranging from **1 to 10**.

#### 4. Sorted Output:

After scoring, the resumes are sorted based on their scores and output in order of best to worst. This ranking is displayed to the user and optionally saved in CSV/JSON formats for further analysis.

## 🚀 Why This Project Matters

This tool demonstrates practical expertise in:

#### 1. Python scripting

#### 2. PDF parsing

#### 3. NLP preprocessing

#### 4. LLM integration (local & API)

#### 5. Prompt engineering

#### 6. Ranking logic & scoring systems

#### 7. Automation for hiring workflows

## 📄 License

MIT License
