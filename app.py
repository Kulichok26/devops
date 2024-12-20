from flask import Flask, request, jsonify
import psycopg2
app = Flask(__name__)

DATABASE = "myapp"
USER = "postgres"
PASSWORD = "EKulikova123"
HOST = "db"
PORT = "5432"

def get_db_connection():
    conn = psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT, options="-c client_encoding=UTF8")
    return conn

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users;')
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['DELETE']) 
def delete_user(user_id): 
    conn = get_db_connection() 
    cursor = conn.cursor() 
    cursor.execute('DELETE FROM users WHERE id = %s;', (user_id,)) 
    conn.commit() 
     
    if cursor.rowcount == 0: 
        return jsonify({'error': 'User  not found'}), 404 
     
    cursor.close() 
    conn.close() 
     
    return jsonify({'message': 'User  deleted successfully'}), 200


@app.route('/')
def home():
    return "Welcome to the user manag. app!"

@app.route('/users', methods=['POST'])
def add_user():
    new_user = request.json
    name = new_user['name']
    email = new_user['email']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
    conn.commit()
    cursor.close()
    conn.close()    
    return jsonify(new_user), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
