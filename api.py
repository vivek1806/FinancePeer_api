from flask import Flask,jsonify
from flask_restful import Resource, Api
from flask_restful import reqparse
from flaskext.mysql import MySQL
import hashlib



mysql = MySQL()
app = Flask(__name__)
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Goldenring@123'
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'


mysql.init_app(app)

api = Api(app)

class Login(Resource):
    def post(self):
        try:
            # Parse the arguments

            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, help='Email address for Authentication')
            parser.add_argument('password', type=str, help='Password for Authentication')
            args = parser.parse_args()

            _userEmail = args['email']
            _userPassword = hashlib.sha256(args['password'].encode('utf-8')).hexdigest()

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_AuthenticateUser',(_userEmail,_userPassword))
            data = cursor.fetchall()
            

            
            if(len(data)>0):
                if(str(data[0][2])==_userEmail):
                    result = {'status':200,'UserId':str(data[0][0])}
                    return jsonify({'result': result})            
                else:
                    result = {'status':100,'message':'Authentication failure'}
                    return jsonify({'result': result}) 
        except Exception as e:
            return {'error': str(e)}
  
            
class CreateUser(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, help='Email address to create user')
            parser.add_argument('password', type=str, help='Password to create user')
            args = parser.parse_args()

            _userEmail = args['email']
            _userPassword = hashlib.sha256(args['password'].encode('utf-8')).hexdigest()

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spCreateUser',(_userEmail,_userPassword))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return {'StatusCode':'200','Message': 'User creation success'}
            else:
                return {'StatusCode':'1000','Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}



api.add_resource(CreateUser, '/CreateUser')
api.add_resource(Login, '/login')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
