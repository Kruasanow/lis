from flask import Flask, render_template, make_response, jsonify, request
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from models import db, Events, Users
from flask_restful import Api, Resource
# from f import is_valid_email, is_valid_name
from datetime import datetime

app = Flask(__name__)

load_dotenv()
DBUSER = os.getenv("DBUSER")
DBUSERPASSWORD = os.getenv("DBUSERPASSWORD")
DBHOST = os.getenv("DBHOST")
DBPORT = os.getenv("DBPORT")
DB = os.getenv("DB")
SECRETKEY = os.getenv("SECRETKEY")

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DBUSER}:{DBUSERPASSWORD}@{DBHOST}:{DBPORT}/{DB}"
app.config['SECRET_KEY'] = SECRETKEY

db.init_app(app) # если выносишь код за контекст этого файла то надо ебашить эту конструкцию
migrate = Migrate(app, db)

api = Api(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/create')
def create():
    return render_template('create.html')

class Login(Resource):
    def post(self):
        data = request.get_json()

        login = data.get('login')
        password = data.get('password')

        from_db_logins = Users.query.all()
        for item in from_db_logins:
            if login in [item.username, item.tg, item.email, item.phone]:
                if password == item.passwords:
                    return make_response(jsonify({'message':'login success'}),200)
                
        return make_response(jsonify({'message':'bad login'}),423)
    
class AddMemoryPlace(Resource):
    def post(self):
        data = request.get_json()  
        try:
            event = Events(
                location= 'location',
                latitude = data.get('latitude'),
                longitude = data.get('longitude'),
                img_ways = data.get('img'),
                description = data.get('description'),
                short_description = data.get('short'),
                story = data.get('story'),
                permission= data.get('privates')
                )
            db.session.add(event)
            db.session.commit()
            return make_response(jsonify({'message':1}),200)
        except Exception as e:
                return make_response(jsonify({'message':f'error - {e}'}),400)

class DelEvent(Resource):
    def delete(self):
        data = request.get_json()
        name = data.get('description')
        email = data.get('email')

        try:
            event = Events.query.filter_by(email=email, descriptions=name).first()
            if event:
                db.session.delete(event)
                db.session.commit()
                return make_response(jsonify({'message':'event deleted'}),200)
            else:
                return make_response(jsonify({'message':'event did not found'}),400)
        except Exception as e:
            return make_response(jsonify({'message':f'error - {e}'}),400)
        
class ChangeEvent(Resource):
    def put(self):
        data = request.get_json()

        try:
            changes = Events.query.filter_by(descriptions=data.get('name')).first()
            for i, j in data.items():
                if hasattr(changes, i):
                    setattr(changes, i, j)
            db.session.commit() # разные поля обновил
            return make_response(jsonify({'message':'data changed', 'data':data}))
        except Exception as e:
            return make_response(jsonify({'message':f'error - {e}'}))
         
api.add_resource(Login,'/api/login')
api.add_resource(AddMemoryPlace,'/api/addevent')
api.add_resource(DelEvent, '/api/delevent')
api.add_resource(ChangeEvent, '/api/changeevent')

if __name__=='__main__':
    app.run(host='0.0.0.0', port='5050', debug=True)