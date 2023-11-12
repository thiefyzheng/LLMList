from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    # Connect to the SQLite database
    conn = sqlite3.connect('models.db')
    c = conn.cursor()

    # Execute the query
    c.execute("SELECT id FROM models LIMIT 5")

    # Fetch the first few rows of the 'id' column
    ids = c.fetchall()

    # Close the connection
    conn.close()

    # Render the ids in the browser
    return render_template_string("""
        <h1>First few IDs:</h1>
        <ul>
        {% for id in ids %}
            <li>{{ id[0] }}</li>
        {% endfor %}
        </ul>
    """, ids=ids)

if __name__ == '__main__':
    app.run(debug=True)
