from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database setup
DATABASE = 'C:\\Users\\Vivien\\Documents\\ChadProxy\\database\\ProxyDB.db'

def connect_db():
    return sqlite3.connect(DATABASE)

# Customer routes
# Customer routes
@app.route('/customers', methods=['GET'])
def get_customers():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM customer')
    customers = cursor.fetchall()

    # Get the column names
    column_names = [desc[0] for desc in cursor.description]

    # Convert the result into a list of dictionaries
    result_list = [dict(zip(column_names, row)) for row in customers]

    connection.close()
    return jsonify(result_list)

@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.json
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO customer (customerId, pseudo, email, password) VALUES (?, ?, ?, ?)',
                   (data['customerId'], data['pseudo'], data['email'], data['password']))
    connection.commit()
    connection.close()
    return jsonify({'message': 'Customer created successfully'})

# Proxy routes
@app.route('/proxies', methods=['GET'])
def get_proxies():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM proxy')
    proxies = cursor.fetchall()

    # Get the column names
    column_names = [desc[0] for desc in cursor.description]

    # Convert the result into a list of dictionaries
    result_list = [dict(zip(column_names, row)) for row in proxies]

    connection.close()
    return jsonify(result_list)

@app.route('/proxies', methods=['POST'])
def create_proxy():
    data = request.json
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO proxy (proxyId, ip, port, type, interface) VALUES (?, ?, ?, ?, ?)',
                   (data['proxyId'], data['ip'], data['port'], data['type'], data['interface']))
    connection.commit()
    connection.close()
    return jsonify({'message': 'Proxy created successfully'})

# CustomerProxy routes
@app.route('/customerproxies', methods=['GET'])
def get_customer_proxies():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM customerproxy')
    customer_proxies = cursor.fetchall()

    # Get the column names
    column_names = [desc[0] for desc in cursor.description]

    # Convert the result into a list of dictionaries
    result_list = [dict(zip(column_names, row)) for row in customer_proxies]

    connection.close()
    return jsonify(result_list)

@app.route('/customerproxies', methods=['POST'])
def create_customer_proxy():
    data = request.json
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO customerproxy (customerId, proxyId, endDate, usedFor) VALUES (?, ?, ?, ?)',
                   (data['customerId'], data['proxyId'], data['endDate'], data['usedFor']))
    connection.commit()
    connection.close()
    return jsonify({'message': 'Customer Proxy created successfully'})

# Additional Proxy routes
@app.route('/proxies/unassigned', methods=['GET'])
def get_unassigned_proxies():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT * FROM proxy
        WHERE proxyId NOT IN (
            SELECT proxyId FROM customerproxy
        )
        OR proxyId IN (
            SELECT proxyId FROM customerproxy
            WHERE endDate < DATE('now')
        )
    ''')
    unassigned_proxies = cursor.fetchall()

    # Get the column names
    column_names = [desc[0] for desc in cursor.description]

    # Convert the result into a list of dictionaries
    result_list = [dict(zip(column_names, row)) for row in unassigned_proxies]

    connection.close()
    return jsonify(result_list)

@app.route('/proxies/unassigned/<used_for>', methods=['GET'])
def get_unassigned_proxies_for_use(used_for):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT * FROM proxy
        WHERE proxyId NOT IN (
            SELECT proxyId FROM customerproxy
            WHERE usedFor = ?
            OR endDate < DATE('now')
        )
    ''', (used_for,))
    unassigned_proxies = cursor.fetchall()

    # Get the column names
    column_names = [desc[0] for desc in cursor.description]

    # Convert the result into a list of dictionaries
    result_list = [dict(zip(column_names, row)) for row in unassigned_proxies]

    connection.close()

@app.route('/customer/<customer_id>/proxies', methods=['GET'])
def get_unassigned_proxies_for_customer(customer_id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT p.proxyId, p.ip, p.port, p.type, p.interface, cp.endDate, cp.usedFor
        FROM proxy p
        LEFT JOIN customerproxy cp ON p.proxyId = cp.proxyId
        WHERE cp.customerId = ?
    ''', (customer_id,))
    unassigned_proxies = cursor.fetchall()

    # Get the column names
    column_names = [desc[0] for desc in cursor.description]

    # Convert the result into a list of dictionaries
    result_list = [dict(zip(column_names, row)) for row in unassigned_proxies]

    connection.close()
    return jsonify(result_list)



if __name__ == '__main__':
    app.run(debug=True)



