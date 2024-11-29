from flask import Flask, render_template, request
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host='db',
        database='mydatabase',
        user='postgres',
        password='postgres'
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM users;')
    users = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', users=users)

@app.route('/query', methods=['GET', 'POST'])
def execute_query():
    if request.method == 'POST':
        query = request.form.get('query')

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(query)
            conn.commit()  # Commit changes for INSERT/UPDATE/DELETE queries

            # Check if the query returns data
            if cur.description:
                results = cur.fetchall()
                columns = [desc[0] for desc in cur.description]
                message = None
            else:
                results = None
                columns = None
                message = f"Query executed successfully. {cur.rowcount} rows affected."
        except Exception as e:
            conn.rollback()
            results = None
            columns = None
            message = f"An error occurred: {e}"
        finally:
            cur.close()
            conn.close()

        return render_template('query_results.html', results=results, columns=columns, message=message)
    else:
        return render_template('query.html')


# @app.route('/query', methods=['GET', 'POST'])
# def execute_query():
#     if request.method == 'POST':
#         query = request.form.get('query')

#         conn = get_db_connection()
#         cur = conn.cursor()
#         try:
#             cur.execute(query)
#             results = cur.fetchall()
#             columns = [desc[0] for desc in cur.description]
#         except Exception as e:
#             conn.rollback()
#             results = []
#             columns = []
#             error_message = f"An error occurred: {e}"
#             return render_template('query_results.html', results=results, columns=columns, error=error_message)
#         finally:
#             cur.close()
#             conn.close()

#         return render_template('query_results.html', results=results, columns=columns)
#     else:
#         return render_template('query.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
