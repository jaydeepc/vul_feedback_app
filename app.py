import os
import webbrowser

import werkzeug
from flask import Flask, render_template, request, json, session, send_file, g, url_for
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'Feedback'
app.config['MYSQL_DATABASE_HOST'] = 'db_server'
app.config['MYSQL_PORT'] = '3306'
mysql.init_app(app)


@app.route("/")
def main():
    if not session.get('logged_in'):
        return render_template('login.html')

    return render_template('login.html')


@app.errorhandler(500)
def handle_internal_server_error(error):
    return str(error)


@app.route('/home', methods=['POST'])
def login():
    _username = request.form['username']
    _password = request.form['inputPassword']

    if _username and _password:
        conn = mysql.connect()
        cursor = conn.cursor()
        all_data = None
        query = "select user_name from tbl_user where user_username='{0}' and user_password='{1}'".format(_username,
                                                                                                          _password)
        try:
            cursor.execute(query)
            data = cursor.fetchone()
        except Exception as ex:
            raise Exception(query, ex)

        # Populate all hotel reviews
        all_data = fetch_reviews(conn, cursor)
        conn.close()

        if data is not None:
            session['logged_in'] = True
            return render_template('index.html', items=all_data, section="hero")
        else:
            return "No user found"

    else:
        return json.dumps({'html': '<span>Enter the required fields</span>'})


def fetch_reviews(conn, cursor):
    query = "select review_hotel, review_city, review_body, review_rating from reviews"
    try:
        cursor.execute(query)
        all_data = cursor.fetchall()
    except:
        conn.rollback()
    return all_data


@app.route('/home/submitted_review', methods=['POST'])
def writeblog():
    _review_hotel = request.form['hotel']
    _review_city = request.form['city']
    _review_body = request.form['review']
    _review_rating = request.form['rating']

    conn = mysql.connect()
    cursor = conn.cursor()
    query = "insert into reviews (review_hotel,  review_city, review_body, review_rating) values ('{0}', '{1}', '{2}', '{3}');".format(
        _review_hotel, _review_city, _review_body, _review_rating)
    try:
        cursor.execute(query)
        conn.commit()
    except:
        conn.rollback()
    conn.close()
    return render_template('index.html')


@app.route('/home', methods=['GET'])
def search():
    if not session.get('logged_in'):
        return render_template('login.html')

    try:
        _search_term = request.args['search_input']
    except werkzeug.exceptions.BadRequest:
        conn = mysql.connect()
        cursor = conn.cursor()
        all_data = fetch_reviews(conn, cursor)
        conn.close()
        return render_template('index.html', items=all_data)
    conn = mysql.connect()
    cursor = conn.cursor()
    query = "select review_hotel, review_city, review_body, review_rating from reviews where review_hotel like '%{0}%' or review_city like '%{0}%' or review_body like '%{0}%'".format(
        _search_term)
    try:
        cursor.execute(query)
        data = cursor.fetchall()
    except:
        conn.rollback()
    conn.close()
    g.search_term = _search_term
    return render_template('index.html', items=data, section="features")


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template('login.html')


@app.route('/home/getfiles', methods=['GET'])
def get_file():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        file = request.args['file']
        return send_file(file)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', debug=True)
