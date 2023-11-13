import requests
import sqlite3
import json

# Define the base URL for the API
base_url = "https://huggingface.co/api/models"

# Define the parameters for the GET request
params = {"author": "TheBloke"}

# Send the GET request
response = requests.get(base_url, params=params)

# Get the JSON response
data = response.json()

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('models.db')

# Create a cursor object
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS models
             (_id text, id text, likes integer, private boolean, downloads integer, tags text, createdAt text, modelId text)''')

num = 0
# Insert or update each model line by line into the database
for model in data:
    # Prepare the data for insertion
    _id = model.get('_id')
    id = model.get('id')
    likes = model.get('likes')
    private = model.get('private')
    downloads = model.get('downloads')
    tags = json.dumps(model.get('tags'))  # Convert the list of tags to a string
    createdAt = model.get('createdAt')
    modelId = model.get('modelId')

    # Check if the model already exists in the database
    c.execute("SELECT * FROM models WHERE _id = ?", (_id,))
    result = c.fetchone()

    if result:
        # If the model exists, update the existing record
        c.execute("UPDATE models SET id = ?, likes = ?, private = ?, downloads = ?, tags = ?, createdAt = ?, modelId = ? WHERE _id = ?",
                  (id, likes, private, downloads, tags, createdAt, modelId, _id))
    else:
        # If the model does not exist, insert a new record
        c.execute("INSERT INTO models VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (_id, id, likes, private, downloads, tags, createdAt, modelId))
        num = num + 1

# Save (commit) the changes
conn.commit()

# Close the connection
conn.close()

print(num)
