# Student Performance Analytics System

A Python-based data analytics project that analyzes student academic performance, calculates grades, identifies top performers, and visualizes results through an interactive Streamlit dashboard.

## 📌 Project Overview

The Student Performance Analytics System helps analyze student marks and attendance to understand academic performance. It uses Python data analysis libraries to process student records and presents insights through an interactive dashboard.

## 🎯 Objectives

- Analyze students' academic marks.
- Calculate total marks and average scores.
- Assign grades based on performance.
- Identify pass and fail status.
- Find top-performing students.
- Analyze subject-wise average marks.
- Display insights using charts and metrics.

## 🛠️ Technologies Used

- **Python** – Core programming language
- **Pandas** – Data processing and analysis
- **NumPy** – Numerical operations
- **Streamlit** – Interactive web application
- **CSV** – Student dataset storage

## 📂 Project Structure

```text
Student-Performance-Analytics/
├── app.py
├── main.py
├── students.csv
├── requirements.txt
└── README.md
```

## 📊 Dataset Description

The `students.csv` file contains student information and academic records.

| Column | Description |
|---|---|
| Student_ID | Unique student identifier |
| Name | Student name |
| Department | Student department |
| Python | Python subject marks |
| AI | Artificial Intelligence marks |
| Maths | Mathematics marks |
| Attendance | Attendance percentage |

## ✨ Features

- Interactive dashboard with performance metrics
- Student records and search functionality
- Subject-wise performance analysis
- Top 3 student performers
- Grade and pass/fail classification
- Data visualization using charts
- CSV report download

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the project folder

```bash
cd Student-Performance-Analytics
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the application

```bash
python -m streamlit run app.py
```

The application will open in your browser. If it does not open automatically, use the local URL displayed in the terminal.

## 🚀 Deployment

This project can be deployed using **Streamlit Community Cloud**.

1. Upload the project files to a GitHub repository.
2. Visit https://share.streamlit.io/
3. Sign in with GitHub.
4. Select your repository and the `app.py` file.
5. Click **Deploy**.

After successful deployment, Streamlit provides a public URL to access the application.

## 🎓 Learning Outcomes

- Practical experience with Python programming
- Data cleaning and analysis using Pandas
- Numerical operations using NumPy
- Interactive dashboard development using Streamlit
- Data visualization and reporting
- GitHub project management and cloud deployment

## 👩‍💻 Author

**Priyanjali Talari**

B.Tech – Computer Science and Engineering (AI & ML)

## 📄 License

This project is intended for educational and learning purposes.
