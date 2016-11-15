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
    return render_template('index.html')


@app.route('/login',methods=['POST'])
def login():
    _username = request.form['username']
    _password = request.form['inputPassword']

    # validate the received values
    if _username and _password:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select user_name from tbl_user where user_username='{0}'".format(_username))
        data = cursor.fetchone()

        if data is not None:
            return render_template('home.html')

    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})


if __name__ == "__main__":
    app.run()

    # select user_name from tbl_user where user_username='admin' or 1=1 '