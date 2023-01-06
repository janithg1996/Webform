import mysql.connector
from flask import Flask, request

app = Flask(__name__)

# Connect to the MySQL database
cnx = mysql.connector.connect(
    host="172.105.49.74",  # Replace with the hostname or IP address of the container running MySQL
    port=5002,  # Replace with the port number that MySQL is listening on
    user="root",  # Replace with the username for the MySQL database
    password="V@lery@#23",  # Replace with the password for the user
    database="appdb"  # Replace with the name of the database you want to connect to
)
cursor = cnx.cursor()

# Create the table
query = """
CREATE TABLE IF NOT EXISTS your-table (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255),
  email VARCHAR(255)
)
"""
cursor.execute(query)
cnx.commit()

# Create the form HTML
form = """
<html>
<body>
<form action="/submit" method="post">
Name: <input type="text" name="name"><br>
Email: <input type="text" name="email"><br>
<input type="submit" value="Submit">
</form>
</body>
</html>
"""

# Display the form
@app.route('/', methods=['GET'])
def display_form():
  return form

# Save the form data to the database
def save_to_database(data):
  try:
    # Insert the form data into the database
    query = "INSERT INTO your-table (name, email) VALUES (%s, %s)"
    cursor.execute(query, data)
    cnx.commit()
  except mysql.connector.Error as err:
    # Print error information
    print("Error: {}".format(err))
  finally:
    cursor.close()
    cnx.close()

# Get the form data from the request
def get_form_data(request):
  data = (request.form['name'], request.form['email'])
  return data

# Handle the form submission
@app.route('/submit', methods=['POST'])
def submit():
  data = get_form_data(request)
  save_to_database(data)
  return 'Success!'

if __name__ == '__main__':
  while True:
    app.run(host='0.0.0.0', port=8080)
