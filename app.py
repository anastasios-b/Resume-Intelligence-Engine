import os
import sys
from pdf_parser import load_pdf_binary
from llm_backend import is_ollama_installed
from ranking_logic import evaluate_candidates_with_llm

# High-level configuration for how we evaluate and rank candidates
TARGET_FIELD = "software engineering"

# IMPORTANT: The total sum of these weights must be 1
WEIGHT_EXPERIENCE = 0.5
WEIGHT_EDUCATION = 0.2
WEIGHT_GENERAL_SKILLS = 0.3

REQUIRED_QUALITIES = {
    # Required education (minimal acceptable baseline)
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

    # General (soft) skills. These are typically boolean/presence-driven traits
    # such as communication, teamwork, and adaptability. Scoring guidance:
    #   - Treat each listed skill as a desirable attribute; presence should add to the
    #     candidate's general-skills score (e.g., 1 if present, 0 if absent), then
    #     normalize across the required set.
    #   - Optionally allow graduates/trainees who show evidence of these skills to gain
    #     partial credit (e.g., project experience or references mentioning the skill).
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

    # Required personal information (e.g. country and city)
    "personal_information": {
        "country": "Greece", # Candidate must live in this country
        "location": "Thessaloniki", # Candidate must live in this country
    }
}

# Good-to-have (optional) qualities — not required but increase ranking.
# If a candidate meets all required qualities and also matches optional ones,
# they should be ranked higher than others with the same base score.
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

# Check for Cloudflare AI configuration before proceeding
if not is_ollama_installed():
    print("ERROR: Cloudflare AI configuration not found. Please set CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID (and optionally CLOUDFLARE_MODEL) in your environment.")
    sys.exit(1)

# Get PDFs from resumes folder
resume_folder = './resumes'
pdf_files = []

if not os.path.isdir(resume_folder):
    print(f"ERROR: Resume folder '{resume_folder}' does not exist.")
    sys.exit(1)

# Iterate through files in resumes folder
for filename in os.listdir(resume_folder):
    if filename.lower().endswith(".pdf"):
        filepath = os.path.join(resume_folder, filename)
        try:
            with open(filepath, "rb") as f:
                pdf_bytes = load_pdf_binary(f)
                pdf_files.append({
                    "filename": filename,
                    "path": filepath,
                    "content": pdf_bytes
                })
                print(f"Loaded: {filename}")
        except Exception as e:
            print(f"WARNING: Failed to load {filename}: {e}")

print(f"\nSuccessfully loaded {len(pdf_files)} PDF file(s).")

# Build ranking configuration from the criteria defined above
config = {
    "target_field": TARGET_FIELD,
    "weights": {
        "experience": WEIGHT_EXPERIENCE,
        "education": WEIGHT_EDUCATION,
        "general_skills": WEIGHT_GENERAL_SKILLS,
    },
    "required_qualities": REQUIRED_QUALITIES,
    "optional_qualities": OPTIONAL_QUALITIES,
}


# Prepare candidates for LLM evaluation
candidates = []
for pdf in pdf_files:
    candidate = {
        "id": pdf["path"],
        "name": pdf["filename"],
        "pdf_preview": pdf["content"].hex()[:100],  # First 100 hex chars
    }
    candidates.append(candidate)


# Stop script here if no candidates for evaluation exist
if not candidates:
    print("No candidates to evaluate.")
    sys.exit(0)


# Invoke ranking logic to evaluate candidates
print(f"\nEvaluating {len(candidates)} candidate(s) using LLM ranking logic...")
try:
    results = evaluate_candidates_with_llm(candidates, config)
except Exception as e:
    print(f"ERROR: Failed during ranking: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


# Display ranked results
print("\n" + "=" * 70)
print("RANKING RESULTS")
print("=" * 70 + "\n")


for rank, result in enumerate(results, start=1):
    name = result.get("name", result.get("id", "Unknown"))
    score = result.get("score_10")
    passed = result.get("passed_required", False)
    explanation = result.get("explanation", "No explanation")
    
    print(f"{rank}. {name}")
    print(f"   Score: {score:.1f}/10" if score is not None else "   Score: N/A")
    print(f"   Passed Required: {'✓ Yes' if passed else '✗ No'}")
    if explanation:
        print(f"   {explanation}")
    if result.get("reasons"):
        print(f"   Details: {', '.join(result['reasons'][:2])}")
    print()


# Save results to file
results_folder = "./results"
if not os.path.exists(results_folder):
    os.makedirs(results_folder)
output_file = os.path.join(results_folder, "ranking_results.txt")
with open(output_file, "w") as f:
    f.write("RESUME RANKING RESULTS\n")
    f.write("=" * 70 + "\n\n")
    for rank, result in enumerate(results, start=1):
        name = result.get("name", result.get("id", "Unknown"))
        score = result.get("score_10")
        passed = result.get("passed_required", False)
        f.write(f"{rank}. {name}\n")
        f.write(f"   Score: {score:.1f}/10\n" if score is not None else "   Score: N/A\n")
        f.write(f"   Passed Required: {'Yes' if passed else 'No'}\n")
        if result.get("explanation"):
            f.write(f"   {result['explanation']}\n")
        f.write("\n")

print(f"\nResults saved to {output_file}")
print("Done! You can now open 'results/ranking_results.txt' to inspect the ranked candidates.")