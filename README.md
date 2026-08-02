# Data Analyst Job Market Analysis — India

An analysis of the data job market in India, focused on Data Analyst roles: skill demand, salary trends, and the intersection of the two, across the country's major tech hubs.

> **Data note:** This analysis runs on a **simulated dataset of 6,000 India-based postings**, generated to match publicly reported 2026 salary benchmarks (Glassdoor, PayScale, Indeed, GROWAI) for role- and city-level pay, and realistic skill-demand patterns across Indian job portals. It is not scraped live posting data. Every figure below is a direct computed output of the pandas/seaborn pipeline in this repo — running `01_generate_data.py` and `02_analysis.py` reproduces every number exactly. Swap in a real posting-level export (e.g. Naukri, LinkedIn, or the Luke Barousse `data_jobs` dataset filtered to India) and the same pipeline will produce real-world figures with zero code changes.

## Summary Dashboard

| Metric | Value |
|---|---|
| Total Jobs Analyzed | 6,000 |
| Data Analyst Jobs | 2,856 |
| Data Scientist Jobs | 1,598 |
| Data Engineer Jobs | 1,546 |
| Skills Analyzed | 20 |
| Cities Covered | 8 |
| Median Salary (All Roles) | ₹13.2 LPA |
| Median Salary (Data Analyst) | ₹8.4 LPA |
| Date Range | Jan 2025 – Dec 2025 |

## The Questions

1. What are the skills most in demand for the top 3 most popular data roles in India?
2. How are in-demand skills trending for Data Analysts?
3. How well do jobs and skills pay for Data Analysts?
4. How do Data Analyst salaries vary across major Indian cities?
5. What are the optimal skills for Data Analysts to learn (high demand **and** high pay)?

## Tools Used

- **Python** — Pandas for analysis, Seaborn/Matplotlib for visualization
- **Jupyter / VS Code** — script and notebook execution
- **Git & GitHub** — version control

## Data Preparation

```python
import pandas as pd

df = pd.read_pickle("data/india_data_jobs.pkl")
df["month"] = df["job_posted_date"].dt.month

# job_skills is a list column; explode to one row per (job, skill)
exploded = df.explode("job_skills").rename(columns={"job_skills": "job_skill"})
```

Dataset schema: `job_id`, `job_title_short`, `job_city`, `job_country`, `job_posted_date`, `experience_level`, `salary_year_lpa`, `job_skills`.

---

## 1. Most In-Demand Skills by Role

For each of the three roles, the top 5 skills by share of postings:

**Data Analyst**
| Skill | % of Postings |
|---|---|
| Excel | 73.6% |
| SQL | 71.9% |
| Python | 41.4% |
| Power BI | 38.1% |
| PowerPoint | 33.0% |

**Data Scientist**
| Skill | % of Postings |
|---|---|
| Python | 81.9% |
| SQL | 65.1% |
| R | 30.2% |
| AWS | 26.7% |
| Git | 23.4% |

**Data Engineer**
| Skill | % of Postings |
|---|---|
| Python | 75.2% |
| SQL | 66.2% |
| Spark | 44.6% |
| AWS | 36.1% |
| Azure | 31.0% |

![Skill demand by role](images/Likelihood_of_Skills_Requested_in_India_Job_Postings.png)

### Insights
- Excel (73.6%) and SQL (71.9%) are the two most-requested skills for Data Analysts, together anchoring the role's baseline skill set.
- Python is the single most-requested skill for Data Scientists, appearing in 81.9% of postings — the highest concentration of any skill across all three roles.
- Data Engineer postings show the heaviest cloud/big-data footprint: Spark (44.6%), AWS (36.1%), and Azure (31.0%) all rank in the top 5, versus none of these appearing in the Data Analyst top 5.

## 2. Skill Trend for Data Analysts (2025)

![Skill trend](images/Trending_Top_Skills_for_Data_Analysts_in_India.png)

| Skill | January | December | Change |
|---|---|---|---|
| Excel | 66.3% | 91.0% | +24.7 pts |
| SQL | 70.9% | 74.1% | +3.2 pts |
| Python | 41.4% | 41.6% | +0.2 pts |
| Power BI | 40.6% | 33.7% | −6.9 pts |
| PowerPoint | 30.7% | 31.9% | +1.2 pts |

### Insights
- Excel shows the largest movement of any tracked skill, rising 24.7 percentage points from January to December and closing the year as the single most-requested skill.
- SQL holds a consistently high share all year (70.9%–74.1%), the most stable of the five tracked skills.
- Power BI is the only skill in the top 5 to decline over the year, falling from 40.6% to 33.7%.

## 3. Salary Analysis

![Salary by role](images/Salary_Distributions_of_Data_Jobs_in_India.png)

| Role | Median Salary |
|---|---|
| Data Engineer | ₹20.92 LPA |
| Data Scientist | ₹18.90 LPA |
| Data Analyst | ₹8.37 LPA |

### Highest Paid vs. Most In-Demand Skills (Data Analyst)

![Highest paid vs in-demand](images/Highest_Paid_and_Most_In_Demand_Skills_for_Data_Analysts_in_India.png)

**Top 5 highest-paid skills:**
| Skill | Median Salary |
|---|---|
| Oracle | ₹10.40 LPA |
| R | ₹9.81 LPA |
| SQL Server | ₹9.78 LPA |
| Python | ₹9.68 LPA |
| SAS | ₹9.63 LPA |

**Top 5 most in-demand skills:**
| Skill | Postings |
|---|---|
| Excel | 2,101 |
| SQL | 2,054 |
| Python | 1,182 |
| Power BI | 1,087 |
| PowerPoint | 943 |

### Insights
- Data Engineer (₹20.92 LPA) and Data Scientist (₹18.90 LPA) postings carry more than double the median salary of Data Analyst postings (₹8.37 LPA).
- Among Data Analyst skills, Oracle commands the highest median salary (₹10.40 LPA) despite ranking outside the top 5 in demand — a clear pay premium for a less common skill.
- Excel and SQL dominate demand (2,101 and 2,054 postings respectively) but sit at the lower end of the pay scale among Data Analyst skills (₹8.10 LPA and ₹8.41 LPA), confirming they are baseline requirements rather than differentiators.

## 4. Salary by City (Data Analyst)

![City salary](images/Median_Data_Analyst_Salary_by_Indian_City.png)

| City | Median Salary | Postings |
|---|---|---|
| Bengaluru | ₹8.93 LPA | 778 |
| Mumbai | ₹8.87 LPA | 367 |
| Delhi NCR | ₹8.51 LPA | 403 |
| Hyderabad | ₹8.45 LPA | 510 |
| Pune | ₹8.00 LPA | 353 |
| Chennai | ₹7.53 LPA | 267 |
| Ahmedabad | ₹6.95 LPA | 79 |
| Kolkata | ₹6.32 LPA | 99 |

### Insights
- Bengaluru posts both the highest median salary (₹8.93 LPA) and the highest posting volume (778) of any city analyzed.
- Mumbai's median salary (₹8.87 LPA) is close behind Bengaluru's despite less than half the posting volume.
- The gap between the highest-paying city (Bengaluru, ₹8.93 LPA) and the lowest (Kolkata, ₹6.32 LPA) is ₹2.61 LPA — a 41% difference.

## 5. Most Optimal Skills for Data Analysts

![Optimal skills](images/Most_Optimal_Skills_for_Data_Analysts_in_India.png)

| Skill | % of Postings | Median Salary | Category |
|---|---|---|---|
| R | 13.8% | ₹9.81 LPA | Programming |
| SQL Server | 15.6% | ₹9.78 LPA | Database |
| Python | 41.4% | ₹9.68 LPA | Programming |
| Tableau | 32.1% | ₹8.99 LPA | Analyst Tool |
| Power BI | 38.1% | ₹8.81 LPA | Analyst Tool |
| SQL | 71.9% | ₹8.41 LPA | Analyst Tool |
| Excel | 73.6% | ₹8.10 LPA | Analyst Tool |
| PowerPoint | 33.0% | ₹7.82 LPA | Analyst Tool |

### Insights
- Python is the standout "optimal" skill: it ranks 3rd-highest in pay (₹9.68 LPA) while appearing in 41.4% of postings — the best balance of demand and salary of any skill analyzed.
- Programming-category skills (R, Python) occupy the top of the pay scale among skills with meaningful demand, both exceeding ₹9.6 LPA median.
- Foundational Analyst Tools (Excel, SQL, PowerPoint) anchor the high-demand, lower-pay end of the chart, confirming they are necessary but not differentiating.

## What I Learned

- **Reproducible pipeline design**: structuring the analysis so every chart and insight traces back to a single computed dataframe made the findings auditable and easy to regenerate.
- **Role-city interaction effects**: salary depends on the combination of role and city, not either factor alone — Data Analyst pay in Bengaluru (₹8.93 LPA) is still well below Data Engineer pay nationally (₹20.92 LPA).
- **Demand ≠ pay**: the highest-demand skills (Excel, SQL) and the highest-paid skills (Oracle, R, SQL Server) are almost entirely disjoint sets, reinforcing that career strategy should weigh both dimensions separately.

## Challenges

- **City name normalization**: Delhi NCR postings needed consolidation (Delhi, Gurugram, Noida) into a single hub category to avoid fragmenting the sample.
- **Skill list explosion**: converting a list-column (`job_skills`) into one row per skill was required before any percentage or salary aggregation could be computed correctly.
- **Calibration against external benchmarks**: tuning the underlying salary model to land within researched real-world ranges (e.g. ₹6.87 LPA national average per Glassdoor, Bengaluru premium of 15–18%) took iteration to avoid an unrealistic distribution.

## Conclusion

Across 6,000 analyzed postings, Excel and SQL are the clear baseline for Data Analyst roles in India, appearing in 73.6% and 71.9% of postings respectively, while Python offers the best combination of demand (41.4%) and pay (₹9.68 LPA median) among all skills studied. Bengaluru leads both in posting volume and salary, and the gap between the highest- and lowest-paying skills for the same role exceeds ₹2 LPA — evidence that skill choice, not just job title, meaningfully shapes earning potential in India's data analytics market.

## Repository Structure

```
├── 01_generate_data.py     # builds the calibrated synthetic dataset
├── 02_analysis.py          # runs all analysis, saves charts + results.json
├── data/
│   ├── india_data_jobs.csv
│   ├── india_data_jobs.pkl
│   └── results.json        # every computed number in this README
└── images/                 # all charts referenced above
```
