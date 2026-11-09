
import streamlit as st

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Grade Manager",
    page_icon="🎓",
    layout="wide"
)

# ==========================================
# CUSTOM CSS - GRADIENT UI
# ==========================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #1e1b4b 50%,
        #312e81 100%
    );
    color: white;
}

.main .block-container {
    padding: 2rem 3rem;
    max-width: 1200px;
}

h1 {
    color: #ffffff !important;
    font-size: 42px !important;
    font-weight: 800 !important;
}

h2, h3, p, label {
    color: #f1f5f9 !important;
}

.subtitle {
    color: #cbd5e1;
    font-size: 17px;
    margin-bottom: 30px;
}

.metric-card {
    background: linear-gradient(
        135deg,
        rgba(99,102,241,0.35),
        rgba(139,92,246,0.15)
    );
    border: 1px solid rgba(255,255,255,0.15);
    padding: 22px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
}

.metric-title {
    color: #c7d2fe;
    font-size: 14px;
    font-weight: 600;
}

.metric-value {
    color: white;
    font-size: 32px;
    font-weight: 800;
    margin-top: 8px;
}

.section-card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 18px;
    padding: 25px;
    margin-bottom: 20px;
}

.stButton > button {
    background: linear-gradient(
        90deg,
        #6366f1,
        #a855f7
    );
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 25px;
    font-weight: 700;
    width: 100%;
    transition: 0.3s;
}

.stButton > button:hover {
    background: linear-gradient(
        90deg,
        #4f46e5,
        #9333ea
    );
    transform: scale(1.02);
    color: white;
}

div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

hr {
    border-color: rgba(255,255,255,0.15);
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# SESSION STATE
# ==========================================

if "students" not in st.session_state:
    st.session_state.students = []


# ==========================================
# GRADE CALCULATION
# ==========================================

def calculate_grade(mark):

    if mark >= 90:
        return "A+"
    elif mark >= 80:
        return "A"
    elif mark >= 70:
        return "B"
    elif mark >= 60:
        return "C"
    elif mark >= 50:
        return "D"
    else:
        return "F"


# ==========================================
# HEADER
# ==========================================

st.markdown("""
<h1>🎓 Grade Manager</h1>

<div class="subtitle">
    Student Performance Dashboard |
    Manage students and monitor academic performance
</div>
""", unsafe_allow_html=True)

st.divider()


# ==========================================
# ADD STUDENT SECTION
# ==========================================

st.markdown("### ➕ Add New Student")

with st.container():

    with st.form("student_form", clear_on_submit=True):

        col1, col2 = st.columns(2)

        with col1:
            student_name = st.text_input(
                "Student Name",
                placeholder="Enter student name"
            )

        with col2:
            student_mark = st.number_input(
                "Student Mark",
                min_value=0,
                max_value=100,
                value=0,
                step=1
            )

        submitted = st.form_submit_button(
            "➕ Add Student"
        )

        if submitted:

            if not student_name.strip():

                st.error("Please enter a student name.")

            else:

                student = {
                    "Name": student_name.strip(),
                    "Mark": student_mark,
                    "Grade": calculate_grade(student_mark)
                }

                st.session_state.students.append(student)

                st.success(
                    f"{student_name} added successfully!"
                )


st.divider()


# ==========================================
# CLASS STATISTICS
# ==========================================

st.markdown("### 📊 Class Performance Overview")

students = st.session_state.students

if students:

    marks = [student["Mark"] for student in students]

    total_students = len(students)

    average = sum(marks) / total_students

    highest = max(marks)

    lowest = min(marks)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">👨‍🎓 Total Students</div>
            <div class="metric-value">{total_students}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">📈 Class Average</div>
            <div class="metric-value">{average:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🏆 Highest Mark</div>
            <div class="metric-value">{highest}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">📉 Lowest Mark</div>
            <div class="metric-value">{lowest}</div>
        </div>
        """, unsafe_allow_html=True)

else:

    st.info("No students added yet. Add your first student above!")


st.divider()


# ==========================================
# STUDENT RESULTS TABLE
# ==========================================

st.markdown("### 📋 Student Results")

if students:

    st.dataframe(
        students,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Name": st.column_config.TextColumn(
                "Student Name"
            ),
            "Mark": st.column_config.NumberColumn(
                "Mark",
                format="%d / 100"
            ),
            "Grade": st.column_config.TextColumn(
                "Grade"
            )
        }
    )

    # ======================================
    # GRADE DISTRIBUTION
    # ======================================

    st.markdown("### 📊 Grade Distribution")

    grade_counts = {}

    for student in students:

        grade = student["Grade"]

        grade_counts[grade] = grade_counts.get(grade, 0) + 1

    st.bar_chart(grade_counts)

    # ======================================
    # CLEAR STUDENT RECORDS
    # ======================================

    st.divider()

    if st.button("🗑️ Clear All Students"):

        st.session_state.students = []

        st.rerun()

else:

    st.markdown("""
    <div class="section-card">
        <h3 style="text-align:center;">
            📚 No Student Records
        </h3>
        <p style="text-align:center;">
            Your student results will appear here
            once you add students.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<br>
<hr>
<p style="text-align:center; color:#94a3b8;">
    🎓 Grade Manager | Built with Python & Streamlit
</p>
""", unsafe_allow_html=True)
