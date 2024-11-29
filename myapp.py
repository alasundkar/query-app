import streamlit as st
import sqlite3
import pandas as pd

# Initialize the database
def init_db():
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')
    c.execute('SELECT COUNT(*) FROM users')
    if c.fetchone()[0] == 0:
        c.executemany('''
            INSERT INTO users (name, email) VALUES (?, ?)
        ''', [
            ('Alice', 'alice@example.com'),
            ('Bob', 'bob@example.com'),
            ('Charlie', 'charlie@example.com')
        ])
        conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('mydatabase.db')
    conn.row_factory = sqlite3.Row
    return conn

def execute_query(query):
    conn = get_db_connection()
    try:
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        if query.strip().upper().startswith('SELECT'):
            rows = c.fetchall()
            columns = [description[0] for description in c.description]
            df = pd.DataFrame(rows, columns=columns)
            return df, None
        else:
            return None, f"Query executed successfully. {c.rowcount} rows affected."
    except Exception as e:
        return None, f"An error occurred: {e}"
    finally:
        conn.close()

# Initialize the database
init_db()

# Streamlit app
st.title("Database Query App")

menu = ["View Users", "Execute Query", "Add User"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "View Users":
    st.subheader("Users List")
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    df_users = pd.DataFrame(users, columns=['id', 'name', 'email'])
    st.dataframe(df_users)

elif choice == "Execute Query":
    st.subheader("Execute SQL Query")
    query = st.text_area("Enter your SQL query:", height=100)
    if st.button("Execute Query"):
        if query.strip() == '':
            st.warning("Please enter a SQL query.")
        else:
            df_result, message = execute_query(query)
            if message:
                st.info(message)
            if df_result is not None and not df_result.empty:
                st.dataframe(df_result)
            elif df_result is not None:
                st.write("Query executed successfully. No results to display.")

elif choice == "Add User":
    st.subheader("Add New User")
    with st.form(key='insert_form'):
        name = st.text_input("Name")
        email = st.text_input("Email")
        submit_button = st.form_submit_button(label='Add User')
    if submit_button:
        if name == '' or email == '':
            st.warning("Please enter both name and email.")
        else:
            insert_query = f"INSERT INTO users (name, email) VALUES ('{name}', '{email}')"
            _, message = execute_query(insert_query)
            st.info(message)
