import streamlit as st
import sqlite3
import pandas as pd

st.header("TODO List (Python + SQLite)")

# ---------------- DB INIT ----------------
conn = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL
)
"""
)
conn.commit()

# ---------------- ADD TASK ----------------
new_task = st.text_input("Add new task")

if st.button("Add"):
    if new_task.strip():
        cursor.execute("INSERT INTO tasks (task) VALUES (?)", (new_task,))
        conn.commit()
        st.rerun()

# ---------------- FETCH TASKS ----------------
cursor.execute("SELECT id, task FROM tasks ORDER BY id ASC")
rows = cursor.fetchall()

if len(rows) == 0:
    st.info("No tasks yet")
    st.stop()

# Real ID (DB) and virtual ids (UI)
db_ids = [r[0] for r in rows]
tasks = [r[1] for r in rows]

display_numbers = list(range(1, len(tasks) + 1))

# Table for showing date
table = {"№": display_numbers, "Task": tasks}
st.dataframe(table, use_container_width=True)


# ---------------- DELETE BY DISPLAY NUMBER ----------------
st.write("### Delete a task by its display number")
delete_display_num = st.number_input(
    "Enter №", min_value=1, max_value=len(tasks), step=1
)

if st.button("Delete"):
    # Get real ID by virtual number
    real_db_id = db_ids[delete_display_num - 1]

    cursor.execute("DELETE FROM tasks WHERE id = ?", (real_db_id,))
    conn.commit()

    st.rerun()
