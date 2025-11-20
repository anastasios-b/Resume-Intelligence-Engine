"""Generate sample software engineer resume PDFs into the `resumes/` folder.

These PDFs are minimal but valid for this project: they start with a %PDF-
header so `load_pdf_binary` accepts them, and they embed realistic resume-like
text content that the LLM can inspect.
"""

import os
from datetime import date


RESUMES = {
    "se_junior_backend_anna_kotsou.pdf": f"""Anna Kotsou\nSoftware Engineer (Junior Backend)\nAthens, Greece\nEmail: anna.kotsou@example.com\nGitHub: github.com/annakotsou\nLinkedIn: linkedin.com/in/annakotsou\n\nSUMMARY\nJunior backend engineer with 2 years of professional Python experience, building APIs and ETL pipelines. Comfortable with AWS and Docker, and eager to grow in machine learning and MLOps.\n\nEXPERIENCE\nPython Backend Engineer, Acme Analytics, Athens  ({date.today().year-2}–present)\n- Developed and maintained REST APIs in Python (FastAPI, Flask).\n- Built ETL jobs that processed millions of rows daily on AWS (Lambda, S3, RDS).\n- Wrote unit and integration tests, improving coverage from 55% to 80%.\n- Collaborated with data science team to productionize ML models.\n\nIntern Software Engineer, DataSoft, Thessaloniki  ({date.today().year-3}–{date.today().year-2})\n- Assisted in migrating a monolithic PHP application to a Python microservice.\n- Implemented small features and bug fixes under senior supervision.\n\nEDUCATION\nBSc Computer Science, Aristotle University of Thessaloniki  ({date.today().year-6}–{date.today().year-2})\n\nSKILLS\n- Languages: Python (2+ years), SQL, Bash\n- Cloud: AWS (Lambda, S3, RDS, CloudWatch)\n- Tools: Docker, Git, Linux\n- Soft skills: teamwork, communication with non-technical stakeholders\n\nLANGUAGES\n- Greek: native\n- English: fluent (C1)\n""",

    "se_mid_fullstack_giorgos_papadopoulos.pdf": f"""Giorgos Papadopoulos\nFull-Stack Software Engineer\nThessaloniki, Greece\nEmail: giorgos.p@example.com\nGitHub: github.com/gpapadopoulos\nLinkedIn: linkedin.com/in/gpapadopoulos\n\nPERSONAL INFORMATION\nCountry: Greece\nLocation: Thessaloniki\nAvailable types of work: remote, hybrid\n\nSUMMARY\nFull-stack engineer with 5+ years of experience building web applications end-to-end, from React frontends to Python/Node.js backends on AWS. Strong focus on clean code, testing, and mentoring junior developers.\n\nEXPERIENCE\nSenior Full-Stack Engineer, FinPay Solutions, Thessaloniki  ({date.today().year-3}–present)\n- Designed and implemented microservices in Python (4 years) using FastAPI and Node.js.\n- Worked extensively with AWS (3+ years) including ECS, RDS, S3, and API Gateway.\n- Collaborated closely with clients, contacting clients directly to gather requirements.\n- Promoted team work and coached junior engineers, showing adaptability to new technologies.\n\nSoftware Engineer, WebCraft Labs, Athens  ({date.today().year-6}–{date.today().year-3})\n- Built internal tools in Django and React to support operations team.\n- Improved SQL queries and indexing, reducing page load times by 40%.\n- Contributed to internal machine learning experiments (2+ years exposure to machine learning workflows).\n\nEDUCATION\nMSc Software Engineering, University of Patras  ({date.today().year-5}–{date.today().year-3})\nBSc Computer Science, University of Patras  ({date.today().year-9}–{date.today().year-5})\n\nSKILLS\n- Specific skills and experience in years:\n  - python: 4 years (backend development)\n  - aws: 3 years (deploying and operating services)\n  - machine learning: 2 years (building and integrating ML-powered features)\n- General skills: contacting clients, team work, adaptability to new technologies\n- Frontend: React, TypeScript, Redux\n- DevOps: AWS, Docker, CI/CD (GitHub Actions)\n- Databases: PostgreSQL, MySQL, Redis\n\nLANGUAGES\n- Greek: conversational\n- English: conversational\n- German: intermediate\n""",

    "se_senior_backend_maria_iliadi.pdf": f"""Maria Iliadi\nSenior Backend Engineer / Tech Lead\nRemote (based in Thessaloniki, Greece)\nEmail: maria.iliadi@example.com\nGitHub: github.com/miliadi\nLinkedIn: linkedin.com/in/mariailiadi\n\nSUMMARY\nSenior backend engineer with 8+ years of experience designing and scaling distributed systems in Python and Go. Led teams of 4–6 engineers and collaborated with product and data teams to deliver features in high-traffic environments.\n\nEXPERIENCE\nTech Lead & Senior Backend Engineer, CloudShip, Remote  ({date.today().year-4}–present)\n- Designed event-driven architecture using AWS SNS/SQS and Lambda.\n- Owned critical microservices written in Python (FastAPI) and Go.\n- Introduced observability stack (Prometheus, Grafana, structured logging).\n- Mentored 5 engineers and ran regular code reviews and architecture sessions.\n\nSenior Software Engineer, DataWave, Athens  ({date.today().year-7}–{date.today().year-4})\n- Implemented large-scale data processing pipelines (Spark, Airflow).\n- Optimized PostgreSQL schemas and queries for analytics workloads.\n\nEDUCATION\nMSc Computer Science, ETH Zurich  ({date.today().year-9}–{date.today().year-7})\nBSc Informatics, Athens University of Economics and Business  ({date.today().year-13}–{date.today().year-9})\n\nSKILLS\n- Languages: Python, Go, SQL\n- Cloud: AWS (ECS, Lambda, RDS, DynamoDB, S3), Terraform\n- Practices: TDD, code reviews, system design\n\nLANGUAGES\n- Greek: native\n- English: fluent (C2)\n""",

    "se_ml_engineer_nikos_petrou.pdf": f"""Nikos Petrou\nMachine Learning Engineer\nThessaloniki, Greece\nEmail: nikos.petrou@example.com\nGitHub: github.com/npetrou\nLinkedIn: linkedin.com/in/nikospetrou\n\nPERSONAL INFORMATION\nCountry: Greece\nLocation: Thessaloniki\nAvailable types of work: remote, hybrid\n\nSUMMARY\nMachine learning engineer with 3+ years of experience building and deploying ML models, focusing on NLP and recommendation systems, primarily in Python. Comfortable working across experimentation and productionization.\n\nEXPERIENCE\nML Engineer, RecoTech, Thessaloniki  ({date.today().year-2}–present)\n- Built recommendation models in Python (3+ years of python experience) using PyTorch and scikit-learn.\n- Deployed models as REST services using FastAPI and Docker on AWS (2+ years of aws experience).\n- Worked with product and sales teams, contacting clients to understand requirements, and demonstrating team work and adaptability to new technologies.\n\nData Scientist, Insight Analytics, Athens  ({date.today().year-4}–{date.today().year-2})\n- Developed NLP models for customer feedback classification (2+ years of machine learning experience).\n- Presented results to stakeholders and helped prioritize product changes.\n\nEDUCATION\nBSc Computer Science, University of Ioannina  ({date.today().year-7}–{date.today().year-3})\n\nSKILLS\n- Specific skills and experience in years:\n  - python: 3 years (production machine learning systems)\n  - aws: 2 years (deploying ML services)\n  - machine learning: 3 years (NLP and recommendation systems)\n- General skills: contacting clients, team work, adaptability to new technologies\n- ML stack: PyTorch, scikit-learn, pandas, NumPy\n- MLOps: Docker, MLflow, AWS S3, Lambda\n- General: Git, Linux, Jupyter\n\nLANGUAGES\n- Greek: conversational\n- English: conversational\n""",

    "se_graduate_trainee_elena_karra.pdf": f"""Elena Karra\nGraduate Software Engineer / Trainee\nThessaloniki, Greece\nEmail: elena.karra@example.com\nGitHub: github.com/elenakarra\nLinkedIn: linkedin.com/in/elenakarra\n\nSUMMARY\nRecent computer science graduate seeking a junior/trainee software engineering role. Strong foundation in Python and web development, with several academic and personal projects.\n\nEDUCATION\nBSc Computer Science, Aristotle University of Thessaloniki  ({date.today().year-4}–{date.today().year})\n- Thesis: "Building a job-matching platform using Python and React"\n- Coursework: algorithms, databases, distributed systems, machine learning\n\nPROJECTS\nJob Matcher (Python, Django, React)\n- Built a job-search web application as part of thesis project.\n- Implemented REST APIs in Django and a React front-end.\n\nPersonal Portfolio Site (Next.js)\n- Created a personal portfolio site with blog and project showcases.\n\nSKILLS\n- Languages: Python, JavaScript/TypeScript, SQL\n- Frameworks: Django, React, Next.js\n- Tools: Git, Docker basics\n\nLANGUAGES\n- Greek: native\n- English: advanced (C1)\n""",
}


def make_minimal_pdf_bytes(text: str) -> bytes:
    """Create minimal PDF bytes with the given text.

    For this project we only need the %PDF- header so `load_pdf_binary` accepts
    the file and the LLM receives reasonable text content. We do not aim for
    full PDF spec compliance.
    """

    # Very simple "PDF": header + plain text body + EOF marker.
    body = "%PDF-1.4\n" + text + "\n%%EOF\n"
    return body.encode("utf-8", errors="replace")


def main() -> None:
    resumes_dir = os.path.join(os.path.dirname(__file__), "resumes")
    os.makedirs(resumes_dir, exist_ok=True)

    for filename, text in RESUMES.items():
        path = os.path.join(resumes_dir, filename)
        data = make_minimal_pdf_bytes(text)
        with open(path, "wb") as f:
            f.write(data)
        print(f"Wrote sample resume: {path}")


if __name__ == "__main__":
    main()
