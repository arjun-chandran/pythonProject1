import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import request


@app.route('/add', methods=['POST'])
def add_student():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        _json = request.json
        _name = _json['name']
        _email = _json['email']
        _phone = _json['phone']
        if _name and _email and _phone and request.method == 'POST':
            sqlQuery = "INSERT INTO student_info(name, email, phone) VALUES(%s, %s, %s)"
            bindData = (_name, _email, _phone)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Student added successfully!')
            respone.status_code = 200
            return respone
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        # if cursor != "None":
        cursor.close()
        # if conn != "None":
        conn.close()


@app.route('/student')
def liststudent():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, name, email, phone FROM student_info")
        studentRows1 = cursor.fetchall()
        respone = jsonify(studentRows1)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/student/<int:id>')
def student(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, name, email, phone FROM student_info WHERE id =%s", id)
        studentRow = cursor.fetchone()
        respone = jsonify(studentRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone


if __name__ == "__main__":
    app.run()
