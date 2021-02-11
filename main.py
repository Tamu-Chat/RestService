import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import psycopg2
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse, abort
from http_status import HttpStatus
from constants import connectionString, hostname
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

@app.route('/api')
def indext():
    return "<center><h1>Tamu Chat API</h1></center>"

@app.errorhandler(404)
def page_not_found(error):
   return "<center><h3>404 Not Found</h3></center>", 404

class TamuChat(Resource):
    def get(self):
        conn = psycopg2.connect(connectionString)
        cur = conn.cursor()
        cur.execute("SELECT * FROM USERS;")
        data = cur.fetchall()
        cur.close()
        conn.close()
        items = []
        for item in data:
            items.append(dict(username=item[1], phonenumber=item[2], uid=item[3], profile_picture=item[4], about=item[5]))
        response = jsonify(items)
        response.status_code = HttpStatus.ok_200
        return response

    def post(self):
        parserManagePosts = reqparse.RequestParser()
        parserManagePosts.add_argument('username')
        parserManagePosts.add_argument('phonenumber')
        parserManagePosts.add_argument('uid')
        parserManagePosts.add_argument('profile_picture')
        parserManagePosts.add_argument('about')
        args = parserManagePosts.parse_args()

        conn = psycopg2.connect(connectionString)
        cur = conn.cursor()

        cur.execute("INSERT INTO USERS (username,phonenumber,uid,profile_pic,about) \
             VALUES ('{}','{}','{}','{}','{}');".format(args['username'],args['phonenumber'],args['uid'],args['profile_picture'],args['about']))
        conn.commit()

        cur.close()
        conn.close()
        return "Succesful", HttpStatus.ok_200

api.add_resource(TamuChat, '/api/tamuChat')

if __name__ == "__main__":
    app.run(host=hostname, port=8686)
