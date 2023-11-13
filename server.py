from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    ids = []
    new_models = []
    search_text = ''
    page = request.args.get('page', 1, type=int)

    # Connect to the SQLite database
    conn = sqlite3.connect('models.db')
    c = conn.cursor()

    if request.method == 'POST':
        search_text = request.form.get('search')

        # Execute the query
        c.execute("SELECT id FROM models WHERE id LIKE ? ORDER BY INSTR(id, ?)", ('%' + search_text + '%', search_text))

        # Fetch all rows of the 'id' column
        ids = c.fetchall()

    # Query for the ten newest models
    c.execute("SELECT id FROM models ORDER BY createdAt DESC")

    # Fetch the ten newest models
    new_models = c.fetchall()

    # Close the connection
    conn.close()

    # Render the ids and the ten newest models in the browser as links to their Hugging Face pages
    return render_template("home.html", ids=ids, new_models=new_models, search_text=search_text, page=page)

if __name__ == '__main__':
    app.run(debug=True)
