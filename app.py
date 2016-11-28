from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL


app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'Feedback'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/")
def main():
    return render_template('login.html')


@app.errorhandler(500)
def handle_internal_server_error(error):
    return str(error)


@app.route('/login',methods=['POST'])
def login():
    _username = request.form['username']
    _password = request.form['inputPassword']

    if _username and _password:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select user_name from tbl_user where user_username='{0}' and user_password='{1}'".format(_username, _password)
        try:
            cursor.execute(query)
            data = cursor.fetchone()
        except Exception as ex:
            raise Exception(query, ex)

        if data is not None:
            return render_template('index.html')
        else:
            return "No user found"

    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})


@app.route('/writereview',methods=['POST'])
def writeblog():
    _review_hotel = request.form['hotel']
    _review_city = request.form['city']
    _review_body = request.form['review']
    _review_rating = request.form['rating']

    conn = mysql.connect()
    cursor = conn.cursor()
    query = "insert into reviews (review_hotel,  review_city, review_body, review_rating) values ('{0}', '{1}', '{2}', '{3}');".format(_review_hotel, _review_city, _review_body, _review_rating)
    try:
        cursor.execute(query)
        conn.commit()
    except:
        conn.rollback()
    conn.close()
    return render_template('success_index.html')

if __name__ == "__main__":
    app.run()
