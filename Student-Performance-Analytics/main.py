"""
Student Performance Analytics System
Uses Python, NumPy and Pandas to analyse student marks.

Run:  python main.py
"""

import numpy as np
import pandas as pd

# ---------- Settings (change the rules here) ----------
SUBJECTS = ["Maths", "Physics", "Chemistry", "English", "Computer_Science"]
PASS_MARK = 40          # minimum marks needed in every subject
MIN_ATTENDANCE = 75     # minimum attendance percentage to pass
DATA_FILE = "students.csv"
OUTPUT_FILE = "student_results.csv"


# ---------- Reusable functions ----------
def load_data(path):
    """Read the CSV file into a DataFrame and show basic information."""
    df = pd.read_csv(path)
    print("Columns :", list(df.columns))
    print("Records :", len(df))
    print("\nFirst 5 records:")
    print(df.head().to_string(index=False))
    print("\nMissing values per column:")
    print(df.isnull().sum().to_string())
    return df


def calculate_total_average(df):
    """Add Total and Average columns using NumPy."""
    marks = df[SUBJECTS].to_numpy()
    df["Total"] = np.sum(marks, axis=1)
    df["Average"] = np.round(np.mean(marks, axis=1), 2)
    return df


def assign_grade(average):
    """Grading rule based on the average marks."""
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    return "F"


def check_result(row):
    """Pass only if every subject >= PASS_MARK and attendance >= MIN_ATTENDANCE."""
    for subject in SUBJECTS:
        if row[subject] < PASS_MARK:
            return "Fail"
    if row["Attendance"] < MIN_ATTENDANCE:
        return "Fail"
    return "Pass"


def add_grades_and_results(df):
    """Use loops to fill Grade, Result and Rank columns."""
    grades = []
    results = []
    for _, row in df.iterrows():
        grades.append(assign_grade(row["Average"]))
        results.append(check_result(row))
    df["Grade"] = grades
    df["Result"] = results
    df["Rank"] = df["Average"].rank(ascending=False, method="min").astype(int)
    return df


def performance_summary(df):
    """Highest, lowest and class average performance."""
    best = df.loc[df["Average"].idxmax()]
    worst = df.loc[df["Average"].idxmin()]
    return {
        "highest_name": best["Name"],
        "highest_avg": best["Average"],
        "lowest_name": worst["Name"],
        "lowest_avg": worst["Average"],
        "class_average": round(float(np.mean(df["Average"])), 2),
    }


def subject_analysis(df):
    """Mean, highest and lowest marks for every subject."""
    rows = []
    for subject in SUBJECTS:
        marks = df[subject].to_numpy()
        rows.append({
            "Subject": subject,
            "Average": round(float(np.mean(marks)), 2),
            "Highest": int(np.max(marks)),
            "Lowest": int(np.min(marks)),
        })
    return pd.DataFrame(rows)


def top_performers(df, n=5):
    """Top n students by average marks."""
    top = df.sort_values("Average", ascending=False).head(n)
    return top[["Rank", "Student_ID", "Name", "Department", "Average", "Grade"]]


def pass_fail_count(df):
    """Number of students who passed and failed."""
    passed = int((df["Result"] == "Pass").sum())
    failed = int((df["Result"] == "Fail").sum())
    return passed, failed


# ---------- Main program ----------
def main():
    print("=" * 60)
    print("        STUDENT PERFORMANCE ANALYTICS SYSTEM")
    print("=" * 60)

    # Step 1: load
    df = load_data(DATA_FILE)

    # Step 2: process
    df = calculate_total_average(df)
    df = add_grades_and_results(df)

    print("\n" + "-" * 60)
    print("STUDENT RESULTS")
    print("-" * 60)
    print(df[["Student_ID", "Name", "Total", "Average",
              "Grade", "Attendance", "Result"]].to_string(index=False))

    # Step 3: analysis
    summary = performance_summary(df)
    print("\n" + "-" * 60)
    print("PERFORMANCE SUMMARY")
    print("-" * 60)
    print(f"Highest average : {summary['highest_name']} ({summary['highest_avg']})")
    print(f"Lowest average  : {summary['lowest_name']} ({summary['lowest_avg']})")
    print(f"Class average   : {summary['class_average']}")

    passed, failed = pass_fail_count(df)
    print(f"\nStudents passed : {passed}")
    print(f"Students failed : {failed}")
    print(f"Pass percentage : {round(passed / len(df) * 100, 2)}%")

    print("\n" + "-" * 60)
    print("GRADE DISTRIBUTION")
    print("-" * 60)
    print(df["Grade"].value_counts().sort_index().to_string())

    print("\n" + "-" * 60)
    print("SUBJECT-WISE ANALYSIS")
    print("-" * 60)
    subjects = subject_analysis(df)
    print(subjects.to_string(index=False))
    best_subject = subjects.loc[subjects["Average"].idxmax(), "Subject"]
    print(f"\nBest performing subject: {best_subject}")

    print("\n" + "-" * 60)
    print("DEPARTMENT-WISE AVERAGE")
    print("-" * 60)
    print(df.groupby("Department")["Average"].mean().round(2).to_string())

    print("\n" + "-" * 60)
    print("TOP 5 PERFORMERS")
    print("-" * 60)
    print(top_performers(df, 5).to_string(index=False))

    # Step 4: save
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nFull results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()