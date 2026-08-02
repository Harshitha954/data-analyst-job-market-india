import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import json

sns.set_theme(style="whitegrid", palette="dark:b_r")
IMG = "/home/claude/project/images"

df = pd.read_pickle("/home/claude/project/data/india_data_jobs.pkl")
df["month"] = df["job_posted_date"].dt.month

exploded = df.explode("job_skills").rename(columns={"job_skills": "job_skill"})

results = {}

# ---------------------------------------------------------------------------
# Q0: Summary dashboard numbers
# ---------------------------------------------------------------------------
results["total_jobs"] = int(len(df))
results["da_jobs"] = int((df["job_title_short"] == "Data Analyst").sum())
results["ds_jobs"] = int((df["job_title_short"] == "Data Scientist").sum())
results["de_jobs"] = int((df["job_title_short"] == "Data Engineer").sum())
results["skills_analyzed"] = int(exploded["job_skill"].nunique())
results["cities_count"] = int(df["job_city"].nunique())
results["median_salary_overall"] = float(df["salary_year_lpa"].median())
results["median_salary_da"] = float(df.loc[df["job_title_short"] == "Data Analyst", "salary_year_lpa"].median())
results["date_range"] = [str(df["job_posted_date"].min().date()), str(df["job_posted_date"].max().date())]

# ---------------------------------------------------------------------------
# Q1: Top 5 skills for top 3 roles
# ---------------------------------------------------------------------------
job_titles = df["job_title_short"].value_counts().index.tolist()  # already top 3 (only 3 exist)
role_totals = df["job_title_short"].value_counts()

skill_counts = exploded.groupby(["job_title_short", "job_skill"]).size().rename("skill_count").reset_index()
skill_counts["skill_percent"] = skill_counts.apply(
    lambda r: 100 * r["skill_count"] / role_totals[r["job_title_short"]], axis=1
)

fig, ax = plt.subplots(len(job_titles), 1, figsize=(8, 10))
top5_by_role = {}
for i, job_title in enumerate(job_titles):
    df_plot = (skill_counts[skill_counts["job_title_short"] == job_title]
               .sort_values("skill_percent", ascending=False).head(5)[::-1])
    top5_by_role[job_title] = df_plot[["job_skill", "skill_percent"]].round(1).to_dict("records")
    sns.barplot(data=df_plot, x="skill_percent", y="job_skill", ax=ax[i], hue="skill_count",
                palette="dark:b_r", legend=False)
    ax[i].set_title(job_title, fontsize=12, fontweight="bold")
    ax[i].set_xlabel("% of Postings" if i == len(job_titles)-1 else "")
    ax[i].set_ylabel("")
    ax[i].xaxis.set_major_formatter(mticker.PercentFormatter())
plt.suptitle("Likelihood of Skills Requested in Indian Job Postings", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{IMG}/Likelihood_of_Skills_Requested_in_India_Job_Postings.png", dpi=150)
plt.close()

results["top5_by_role"] = top5_by_role

# ---------------------------------------------------------------------------
# Q2: Skill trend for Data Analysts by month
# ---------------------------------------------------------------------------
da_exploded = exploded[exploded["job_title_short"] == "Data Analyst"]
da_monthly_total = df[df["job_title_short"] == "Data Analyst"].groupby("month").size()

top5_da_skills = (da_exploded["job_skill"].value_counts().head(5).index.tolist())
trend = (da_exploded[da_exploded["job_skill"].isin(top5_da_skills)]
         .groupby(["month", "job_skill"]).size().unstack(fill_value=0))
trend_pct = trend.div(da_monthly_total, axis=0) * 100
trend_pct = trend_pct[top5_da_skills]  # keep order = overall rank

plt.figure(figsize=(9, 5))
sns.lineplot(data=trend_pct, dashes=False, palette="tab10")
plt.gca().yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
plt.title("Trending Top Skills for Data Analysts in India (2025)", fontsize=13, fontweight="bold")
plt.xlabel("Month")
plt.ylabel("% of Postings")
plt.xticks(range(1, 13))
plt.legend(title="Skill", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
plt.savefig(f"{IMG}/Trending_Top_Skills_for_Data_Analysts_in_India.png", dpi=150)
plt.close()

results["da_skill_trend_start_end"] = {
    skill: {"jan": round(trend_pct[skill].iloc[0], 1), "dec": round(trend_pct[skill].iloc[-1], 1)}
    for skill in top5_da_skills
}

# ---------------------------------------------------------------------------
# Q3a: Salary distribution across roles (box plot)
# ---------------------------------------------------------------------------
job_order = df.groupby("job_title_short")["salary_year_lpa"].median().sort_values(ascending=False).index

plt.figure(figsize=(9, 4.5))
sns.boxplot(data=df, x="salary_year_lpa", y="job_title_short", order=job_order, hue="job_title_short",
            palette="dark:b_r", legend=False)
plt.gca().xaxis.set_major_formatter(mticker.FuncFormatter(lambda y, pos: f"₹{y:.0f}L"))
plt.title("Salary Distributions of Data Jobs in India", fontsize=13, fontweight="bold")
plt.xlabel("Median Annual Salary")
plt.ylabel("")
plt.tight_layout()
plt.savefig(f"{IMG}/Salary_Distributions_of_Data_Jobs_in_India.png", dpi=150)
plt.close()

results["salary_by_role"] = df.groupby("job_title_short")["salary_year_lpa"].median().round(2).to_dict()

# ---------------------------------------------------------------------------
# Q3b: Highest paid vs most in-demand skills for Data Analysts
# ---------------------------------------------------------------------------
da_only_exploded = exploded[exploded["job_title_short"] == "Data Analyst"]
da_skill_stats = da_only_exploded.groupby("job_skill").agg(
    median_salary=("salary_year_lpa", "median"),
    count=("salary_year_lpa", "size")
)
da_skill_stats["skill_percent"] = 100 * da_skill_stats["count"] / results["da_jobs"]

top_pay = da_skill_stats.sort_values("median_salary", ascending=False).head(10)
top_demand = da_skill_stats.sort_values("count", ascending=False).head(10)

fig, ax = plt.subplots(2, 1, figsize=(8, 9))
sns.barplot(data=top_pay.reset_index(), x="median_salary", y="job_skill", hue="median_salary",
            ax=ax[0], palette="dark:b_r", legend=False)
ax[0].set_title("Top 10 Highest Paid Skills for Data Analysts (India)", fontweight="bold")
ax[0].set_xlabel("Median Salary (₹ LPA)")
ax[0].set_ylabel("")

sns.barplot(data=top_demand.reset_index(), x="count", y="job_skill", hue="count",
            ax=ax[1], palette="light:b", legend=False)
ax[1].set_title("Top 10 Most In-Demand Skills for Data Analysts (India)", fontweight="bold")
ax[1].set_xlabel("Number of Postings")
ax[1].set_ylabel("")
plt.tight_layout()
plt.savefig(f"{IMG}/Highest_Paid_and_Most_In_Demand_Skills_for_Data_Analysts_in_India.png", dpi=150)
plt.close()

results["top_pay_skills"] = top_pay["median_salary"].round(2).to_dict()
results["top_demand_skills"] = top_demand["count"].to_dict()

# ---------------------------------------------------------------------------
# Q4: City comparison for Data Analysts
# ---------------------------------------------------------------------------
da_df = df[df["job_title_short"] == "Data Analyst"]
city_salary = da_df.groupby("job_city")["salary_year_lpa"].median().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
sns.barplot(x=city_salary.values, y=city_salary.index, hue=city_salary.index,
            palette="mako", legend=False)
plt.gca().xaxis.set_major_formatter(mticker.FuncFormatter(lambda y, pos: f"₹{y:.0f}L"))
plt.title("Median Data Analyst Salary by Indian City", fontsize=13, fontweight="bold")
plt.xlabel("Median Annual Salary")
plt.ylabel("")
plt.tight_layout()
plt.savefig(f"{IMG}/Median_Data_Analyst_Salary_by_Indian_City.png", dpi=150)
plt.close()

results["city_salary_da"] = city_salary.round(2).to_dict()
results["city_job_counts"] = da_df["job_city"].value_counts().to_dict()

# ---------------------------------------------------------------------------
# Q5: Optimal skills scatter (demand >= 5th percentile threshold, i.e. common enough)
# ---------------------------------------------------------------------------
skill_category = {k: v[0] for k, v in {
    "SQL": ("Analyst Tool", 0), "Excel": ("Analyst Tool", 0), "PowerPoint": ("Analyst Tool", 0),
    "Power BI": ("Analyst Tool", 0), "Tableau": ("Analyst Tool", 0), "Python": ("Programming", 0),
    "R": ("Programming", 0), "SAS": ("Programming", 0), "SQL Server": ("Database", 0), "Oracle": ("Database", 0),
    "Git": ("Programming", 0),
}.items()}

da_skill_stats_reset = da_skill_stats.reset_index()
da_skill_stats_reset["technology"] = da_skill_stats_reset["job_skill"].map(skill_category).fillna("Other")

high_demand = da_skill_stats_reset[da_skill_stats_reset["count"] >= da_skill_stats_reset["count"].quantile(0.25)]

plt.figure(figsize=(8, 6))
scatter = sns.scatterplot(data=high_demand, x="skill_percent", y="median_salary", hue="technology",
                           palette="bright", s=110, legend="full")
for _, row in high_demand.iterrows():
    plt.text(row["skill_percent"] + 0.4, row["median_salary"], row["job_skill"], fontsize=8)
plt.gca().xaxis.set_major_formatter(mticker.PercentFormatter())
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, pos: f"₹{y:.0f}L"))
plt.title("Most Optimal Skills for Data Analysts in India", fontsize=13, fontweight="bold")
plt.xlabel("% of Data Analyst Postings")
plt.ylabel("Median Salary")
plt.tight_layout()
plt.savefig(f"{IMG}/Most_Optimal_Skills_for_Data_Analysts_in_India.png", dpi=150)
plt.close()

results["optimal_skills"] = high_demand.sort_values("median_salary", ascending=False)[
    ["job_skill", "skill_percent", "median_salary", "technology"]
].round(2).to_dict("records")

with open("/home/claude/project/data/results.json", "w") as f:
    json.dump(results, f, indent=2, default=str)

print("DONE")
print(json.dumps({k: results[k] for k in ["total_jobs", "da_jobs", "ds_jobs", "de_jobs",
                                            "skills_analyzed", "cities_count",
                                            "median_salary_overall", "median_salary_da"]}, indent=2))
