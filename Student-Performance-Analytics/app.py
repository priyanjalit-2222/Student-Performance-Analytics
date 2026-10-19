
from pathlib import Path

import pandas as pd
import streamlit as st

import main as core

st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="🎓",
    layout="wide"
)


@st.cache_data
def prepare(df):
    df = core.calculate_total_average(df.copy())
    df = core.add_grades_and_results(df)
    return df


st.sidebar.header("Data")

uploaded = st.sidebar.file_uploader(
    "Upload a students CSV (optional)",
    type=["csv"]
)

csv_path = Path(__file__).parent / "students.csv"

try:
    if uploaded is not None:
        raw = pd.read_csv(uploaded)
    else:
        raw = pd.read_csv(csv_path)
except FileNotFoundError:
    st.error(
        "Could not find students.csv. "
        "Make sure it is uploaded to the same GitHub folder as app.py."
    )
    st.stop()
except pd.errors.EmptyDataError:
    st.error("The CSV file is empty. Please upload a valid dataset.")
    st.stop()
except pd.errors.ParserError:
    st.error("The CSV file format is invalid. Please check the file.")
    st.stop()

missing = [
    c for c in core.SUBJECTS + [
        "Student_ID",
        "Name",
        "Department",
        "Attendance"
    ]
    if c not in raw.columns
]

if missing:
    st.error(f"The CSV is missing these columns: {', '.join(missing)}")
    st.stop()

df = prepare(raw)

st.sidebar.header("Filters")

departments = st.sidebar.multiselect(
    "Department",
    sorted(df["Department"].dropna().unique()),
    default=sorted(df["Department"].dropna().unique())
)

result_filter = st.sidebar.radio(
    "Result",
    ["All", "Pass", "Fail"],
    horizontal=True
)

view = df[df["Department"].isin(departments)]

if result_filter != "All":
    view = view[view["Result"] == result_filter]

st.title("🎓 Student Performance Analytics System")

st.caption(
    f"Pass rule: at least {core.PASS_MARK} in every subject and "
    f"{core.MIN_ATTENDANCE}% attendance."
)

if view.empty:
    st.warning("No students match the selected filters.")
    st.stop()

summary = core.performance_summary(view)
passed, failed = core.pass_fail_count(view)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Students", len(view))
c2.metric("Class Average", summary["class_average"])
c3.metric("Passed / Failed", f"{passed} / {failed}")
c4.metric(
    "Top Student",
    summary["highest_name"],
    f"{summary['highest_avg']} average"
)

tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Results",
    "📊 Subject Analysis",
    "🏆 Top Performers",
    "🔍 Student Lookup"
])

with tab1:
    st.subheader("Student Results")

    st.dataframe(
        view[
            [
                "Student_ID",
                "Name",
                "Department",
                "Total",
                "Average",
                "Grade",
                "Attendance",
                "Result",
                "Rank"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Results as CSV",
        data=view.to_csv(index=False).encode("utf-8"),
        file_name="student_results.csv",
        mime="text/csv"
    )

with tab2:
    subjects = core.subject_analysis(view)

    left, right = st.columns(2)

    with left:
        st.subheader("Average Marks by Subject")
        st.bar_chart(subjects.set_index("Subject")["Average"])

        best = subjects.loc[
            subjects["Average"].idxmax(),
            "Subject"
        ]

        st.success(f"Best Performing Subject: {best}")

    with right:
        st.subheader("Subject Details")
        st.dataframe(
            subjects,
            use_container_width=True,
            hide_index=True
        )

    left, right = st.columns(2)

    with left:
        st.subheader("Grade Distribution")
        st.bar_chart(df["Grade"].value_counts().sort_index())

    with right:
        st.subheader("Department Average")
        st.bar_chart(
            view.groupby("Department")["Average"].mean().round(2)
        )

with tab3:
    st.subheader("Top Performing Students")

    maximum = min(10, len(view))
    default_n = min(5, maximum)

    n = st.slider(
        "Number of students",
        min_value=1,
        max_value=maximum,
        value=default_n
    )

    st.dataframe(
        core.top_performers(view, n),
        use_container_width=True,
        hide_index=True
    )

with tab4:
    st.subheader("Search Student Performance")

    names = sorted(view["Name"].dropna().unique())

    if names:
        name = st.selectbox("Select a student", names)

        student = view[view["Name"] == name].iloc[0]

        a, b, c = st.columns(3)

        a.metric("Average", student["Average"])
        b.metric("Grade", student["Grade"])
        c.metric("Result", student["Result"])

        st.write(
            f"**Student ID:** {student['Student_ID']}  \n"
            f"**Department:** {student['Department']}  \n"
            f"**Attendance:** {student['Attendance']}%  \n"
            f"**Rank:** {student['Rank']}"
        )

        st.subheader("Subject Marks")
        st.bar_chart(student[core.SUBJECTS].astype(float))
    else:
        st.info("No student names are available in this selection.")
