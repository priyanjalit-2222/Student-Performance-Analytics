"""
Student Performance Analytics - Streamlit frontend.
Reuses the functions from main.py.

Run:  streamlit run app.py
"""

import pandas as pd
import streamlit as st

import main as core  # functions and settings from main.py

st.set_page_config(page_title="Student Performance Analytics", page_icon="🎓", layout="wide")


@st.cache_data
def prepare(df):
    """Run the full processing pipeline from main.py on a DataFrame."""
    df = core.calculate_total_average(df.copy())
    df = core.add_grades_and_results(df)
    return df


# ---------- Sidebar: data source and filters ----------
st.sidebar.header("Data")
uploaded = st.sidebar.file_uploader("Upload a students CSV (optional)", type="csv")
try:
    raw = pd.read_csv(uploaded) if uploaded else pd.read_csv(core.DATA_FILE)
except FileNotFoundError:
    st.error(f"Could not find {core.DATA_FILE}. Keep it in the same folder as app.py.")
    st.stop()

missing = [c for c in core.SUBJECTS + ["Student_ID", "Name", "Department", "Attendance"]
           if c not in raw.columns]
if missing:
    st.error(f"The CSV is missing these columns: {', '.join(missing)}")
    st.stop()

df = prepare(raw)

st.sidebar.header("Filters")
departments = st.sidebar.multiselect(
    "Department", sorted(df["Department"].unique()), default=sorted(df["Department"].unique()))
result_filter = st.sidebar.radio("Result", ["All", "Pass", "Fail"], horizontal=True)

view = df[df["Department"].isin(departments)]
if result_filter != "All":
    view = view[view["Result"] == result_filter]

# ---------- Header and summary cards ----------
st.title("🎓 Student Performance Analytics System")
st.caption(f"Pass rule: at least {core.PASS_MARK} in every subject and "
           f"{core.MIN_ATTENDANCE}% attendance.")

if view.empty:
    st.warning("No students match the selected filters.")
    st.stop()

summary = core.performance_summary(view)
passed, failed = core.pass_fail_count(view)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Students", len(view))
c2.metric("Class average", summary["class_average"])
c3.metric("Passed / Failed", f"{passed} / {failed}")
c4.metric("Top student", summary["highest_name"], f"{summary['highest_avg']} avg")

# ---------- Tabs ----------
tab1, tab2, tab3, tab4 = st.tabs(
    ["📋 Results", "📊 Subject analysis", "🏆 Top performers", "🔍 Student lookup"])

with tab1:
    st.dataframe(
        view[["Student_ID", "Name", "Department", "Total", "Average",
              "Grade", "Attendance", "Result", "Rank"]],
        width="stretch", hide_index=True)
    st.download_button("Download results as CSV", view.to_csv(index=False),
                       file_name="student_results.csv", mime="text/csv")

with tab2:
    subjects = core.subject_analysis(view)
    left, right = st.columns(2)
    with left:
        st.subheader("Average marks by subject")
        st.bar_chart(subjects.set_index("Subject")["Average"])
        best = subjects.loc[subjects["Average"].idxmax(), "Subject"]
        st.success(f"Best performing subject: {best}")
    with right:
        st.subheader("Subject details")
        st.dataframe(subjects, width="stretch", hide_index=True)

    left, right = st.columns(2)
    with left:
        st.subheader("Grade distribution")
        st.bar_chart(view["Grade"].value_counts().sort_index())
    with right:
        st.subheader("Department average")
        st.bar_chart(view.groupby("Department")["Average"].mean().round(2))

with tab3:
    n = st.slider("How many students?", 3, min(10, len(view)), min(5, len(view))) \
        if len(view) > 3 else len(view)
    st.dataframe(core.top_performers(view, n), width="stretch", hide_index=True)

with tab4:
    name = st.selectbox("Select a student", view["Name"].tolist())
    student = view[view["Name"] == name].iloc[0]
    a, b, c = st.columns(3)
    a.metric("Average", student["Average"])
    b.metric("Grade", student["Grade"])
    c.metric("Result", student["Result"])
    st.write(f"**ID:** {student['Student_ID']}  |  **Department:** {student['Department']}  |  "
             f"**Attendance:** {student['Attendance']}%  |  **Rank:** {student['Rank']}")
    st.bar_chart(student[core.SUBJECTS].astype(int))