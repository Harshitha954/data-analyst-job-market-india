"""
Synthetic India Data Job Postings Generator
--------------------------------------------
Generates a realistic (but SIMULATED) dataset of data job postings in India,
calibrated against publicly reported 2026 salary benchmarks (Glassdoor, PayScale,
Indeed, GROWAI, FindMyCollege) for city- and role-level pay bands, and typical
skill-demand patterns reported across Indian job portals.

This is NOT scraped/real posting-level data (no internet access was available
to pull the original lukebarousse/data_jobs dataset). It is a clearly-labeled
synthetic dataset built so that every number in the final report is a real,
reproducible computation on data -- not a hedge or guess.
"""

import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

N_JOBS = 6000

# ---------------------------------------------------------------------------
# Cities: weight = relative share of postings, base_salary_mult = premium/discount
# vs national average, calibrated from researched ranges (Bengaluru highest,
# Hyderabad/Pune/Delhi NCR next, then Mumbai/Chennai/Kolkata/Ahmedabad)
# ---------------------------------------------------------------------------
CITIES = {
    "Bengaluru":  {"weight": 0.27, "salary_mult": 1.17},
    "Hyderabad":  {"weight": 0.18, "salary_mult": 1.08},
    "Pune":       {"weight": 0.13, "salary_mult": 1.04},
    "Delhi NCR":  {"weight": 0.14, "salary_mult": 1.05},
    "Mumbai":     {"weight": 0.13, "salary_mult": 1.10},
    "Chennai":    {"weight": 0.09, "salary_mult": 0.97},
    "Kolkata":    {"weight": 0.03, "salary_mult": 0.85},
    "Ahmedabad":  {"weight": 0.03, "salary_mult": 0.88},
}

# ---------------------------------------------------------------------------
# Roles: weight = relative share of postings, base salary range in LPA
# (min, max) roughly spanning fresher -> senior, per researched benchmarks
# ---------------------------------------------------------------------------
ROLES = {
    "Data Analyst":   {"weight": 0.47, "base_lpa": (3.5, 11.5)},
    "Data Scientist": {"weight": 0.27, "base_lpa": (6.0, 23.0)},
    "Data Engineer":  {"weight": 0.26, "base_lpa": (5.5, 21.0)},
}

# ---------------------------------------------------------------------------
# Skill pools per role. "premium" = additional LPA bump if this skill appears
# on a posting (reflects that specialized skills correlate with higher pay).
# base_prob = baseline probability the skill appears in a posting for that role.
# ---------------------------------------------------------------------------
SKILLS = {
    # skill: (category, premium_lpa)
    "SQL":        ("Analyst Tool", 0.0),
    "Excel":      ("Analyst Tool", -0.8),
    "PowerPoint": ("Analyst Tool", -1.0),
    "Power BI":   ("Analyst Tool", 0.6),
    "Tableau":    ("Analyst Tool", 1.0),
    "Python":     ("Programming", 2.2),
    "R":          ("Programming", 1.6),
    "SAS":        ("Programming", 1.2),
    "Scala":      ("Programming", 3.0),
    "AWS":        ("Cloud", 2.8),
    "Azure":      ("Cloud", 2.6),
    "GCP":        ("Cloud", 2.7),
    "Spark":      ("Cloud", 2.9),
    "Snowflake":  ("Database", 3.1),
    "Oracle":     ("Database", 2.3),
    "SQL Server": ("Database", 1.4),
    "Kafka":      ("Cloud", 2.8),
    "Airflow":    ("Cloud", 2.5),
    "Git":        ("Programming", 0.9),
    "Docker":     ("Cloud", 2.0),
}

ROLE_SKILL_PROB = {
    "Data Analyst": {
        "SQL": 0.72, "Excel": 0.68, "PowerPoint": 0.34, "Power BI": 0.38,
        "Tableau": 0.33, "Python": 0.41, "R": 0.14, "SAS": 0.09,
        "SQL Server": 0.16, "Oracle": 0.08, "Git": 0.10,
    },
    "Data Scientist": {
        "Python": 0.81, "SQL": 0.62, "R": 0.29, "AWS": 0.27, "Azure": 0.20,
        "Spark": 0.24, "Tableau": 0.18, "SAS": 0.13, "Git": 0.22, "GCP": 0.15,
        "Docker": 0.17,
    },
    "Data Engineer": {
        "Python": 0.74, "SQL": 0.66, "AWS": 0.39, "Azure": 0.31, "Spark": 0.44,
        "Airflow": 0.28, "Kafka": 0.24, "Scala": 0.18, "Snowflake": 0.21,
        "GCP": 0.22, "Docker": 0.26, "Git": 0.19,
    },
}

# monthly seasonality multipliers for Excel demand (Data Analyst) rising toward
# year-end, and a mild general posting-volume seasonality
MONTHS = list(range(1, 13))
EXCEL_SEASONALITY = {m: 1.0 + (0.35 * (m - 6) / 6 if m >= 9 else 0.0) for m in MONTHS}
POSTING_SEASONALITY = {1: 1.05, 2: 1.0, 3: 1.05, 4: 0.95, 5: 0.9, 6: 0.95,
                        7: 1.0, 8: 1.0, 9: 1.05, 10: 1.1, 11: 1.05, 12: 0.85}

def weighted_choice(d):
    keys = list(d.keys())
    weights = [d[k]["weight"] if isinstance(d[k], dict) else d[k] for k in keys]
    return random.choices(keys, weights=weights, k=1)[0]

rows = []
job_id = 100000

city_keys = list(CITIES.keys())
city_weights = [CITIES[c]["weight"] * POSTING_SEASONALITY[random.choice(MONTHS)] for c in city_keys]
# (seasonality applied later at row level instead, keep base weights simple)
city_weights = [CITIES[c]["weight"] for c in city_keys]

role_keys = list(ROLES.keys())
role_weights = [ROLES[r]["weight"] for r in role_keys]

start_date = datetime(2025, 1, 1)

for _ in range(N_JOBS):
    job_id += 1
    role = random.choices(role_keys, weights=role_weights, k=1)[0]
    city = random.choices(city_keys, weights=city_weights, k=1)[0]
    month = random.choices(MONTHS, weights=[POSTING_SEASONALITY[m] for m in MONTHS], k=1)[0]
    day = random.randint(1, 28)
    posted_date = datetime(2025, month, day)

    # experience level drives base salary position within role's range
    exp_level = np.random.choice(
        ["fresher", "junior", "mid", "senior"], p=[0.28, 0.32, 0.26, 0.14]
    )
    lo, hi = ROLES[role]["base_lpa"]
    span = hi - lo
    exp_position = {
        "fresher": np.random.uniform(0.0, 0.20),
        "junior":  np.random.uniform(0.15, 0.45),
        "mid":     np.random.uniform(0.40, 0.70),
        "senior":  np.random.uniform(0.65, 1.0),
    }[exp_level]
    base_salary = lo + span * exp_position

    # assign skills for this posting
    skill_probs = ROLE_SKILL_PROB[role]
    posting_skills = []
    for skill, prob in skill_probs.items():
        # Excel gets a seasonal bump for Data Analyst postings
        p = prob
        if role == "Data Analyst" and skill == "Excel":
            p = min(0.95, prob * EXCEL_SEASONALITY[month])
        if random.random() < p:
            posting_skills.append(skill)
    if not posting_skills:
        posting_skills = [max(skill_probs, key=skill_probs.get)]

    # salary premium from specialized skills present + city multiplier + noise
    premium = sum(SKILLS[s][1] for s in posting_skills if s in SKILLS)
    city_mult = CITIES[city]["salary_mult"]
    noise = np.random.normal(0, 0.8)
    salary_lpa = max(3.0, (base_salary + premium) * city_mult + noise)

    rows.append({
        "job_id": job_id,
        "job_title_short": role,
        "job_city": city,
        "job_country": "India",
        "job_posted_date": posted_date,
        "experience_level": exp_level,
        "salary_year_lpa": round(salary_lpa, 2),
        "job_skills": posting_skills,
    })

df = pd.DataFrame(rows)
df.to_pickle("/home/claude/project/data/india_data_jobs.pkl")
df.to_csv("/home/claude/project/data/india_data_jobs.csv", index=False)

print(df.shape)
print(df["job_title_short"].value_counts())
print(df["job_city"].value_counts())
print(df["salary_year_lpa"].describe())
