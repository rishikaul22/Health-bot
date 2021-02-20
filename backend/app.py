from flask import Flask, request, jsonify
import pymongo
from flask_restful import Resource, Api
import numpy as np
from datetime import datetime
from prediction import prediction

##################### Setting up flask app #####################
app = Flask(__name__)
app.config['SECRET_KEY'] = 'healthbot'

##################### Setting up mongo-DB database #####################
connection_url = 'mongodb+srv://priyavmehta:priyavmehta@health-bot.pe09f.mongodb.net/<healthbot>?retryWrites=true&w=majority'
client = pymongo.MongoClient(connection_url)

# Database Name
Database = client.get_database('healthbot')

# Tables Name
UserTable = Database.Users

class UserRegister(Resource):

    def post(self):

        data = request.get_json()
        email = data['email']

        user = UserTable.find_one({'email': email})

        if user :
            return { "msg" : "This email id already exists" }

        userObject = {
            "name" : data["name"],
            "password": data["password"],
            "number" : data["number"],
            "email" : data["email"],
            "diabetes" : data["diabetes"],
            "blood_pressure" : data["blood_pressure"],
            "frequent_cold" : data["frequent_cold"],
            "frequent_cough" : data["frequent_cough"],
            "migraine" : data["migraine"]
        }
        query = UserTable.insert_one(userObject)
        return { "msg" : "User registered successfully" }

class UserLogin(Resource):
    
    def post(self):

        data = request.get_json()
        email = data['email']
        password = data['password']

        user = UserTable.find_one({'email': email})

        if user:

            if password == user['password']:

                userDetails = {
                    "name" : user["name"],
                    "password": user["password"],
                    "number" : user["number"],
                    "email" : user["email"],
                    "diabetes" :user["diabetes"],
                    "blood_pressure" : user["blood_pressure"],
                    "frequent_cold" : user["frequent_cold"],
                    "frequent_cough" : user["frequent_cough"],
                    "migraine" : user["migraine"]
                }
                
                return { "msg" : "Login successful", 'user': userDetails }

            return { "msg" : "Invalid Credentials" }

        return { "msg" : "User does not exist...!!!"}

class Prediction(Resource):

    def post(self):

        data = request.get_json()
        symptoms = data["symptoms"]
        email = data["email"]
        user = UserTable.find_one({'email': email})
        diseases = prediction(symptoms, user)
        return diseases

api = Api(app)
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(Prediction, '/predict')

# fever
# headache
# skin itching
# throat pain

# 1,2,3,4,5
# 1,2,3,4
# 2,4
# 5

# arthritis : 4/6 => 67 %
# malaria : 5/6 => 82 %
# hepatitis : 7/9 => 77 %

# Malaria : [Chills, fever, sweating, shivering, nausea, vomiting, fast heart rate, headache] => 75 %
# Mumps : [Swollen /painful salivary glands, fever, headache, fatigue, appetite loss, difficulty in swallowing or soreness, neck swelling.], => 20 %
# Lung Cancer : [Cough, chest pain, wheezing and weight loss.] => 0 %

# 1,2
# 1,2
# 1
# 3
# Ans : 1

if __name__ == '__main__':
    app.run(debug=True)