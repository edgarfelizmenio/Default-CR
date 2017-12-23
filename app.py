from flask import Flask
from flask_restful import Api

app=Flask(__name__)
api = Api(app)
# import data model

# import rest api

# from flask_restful import Resource, Api



# class Patient(Resource):
#     def get(self):
#         return {'paktu':'ka'}

# api.add_resource(Patient, '/patient')



import database

@app.teardown_appcontext
def shutdown_session(Exception=None):
    database.db_session.remove()

import resources

api.add_resource(resources.Persons, '/person')
api.add_resource(resources.Person, '/person/<int:person_id>')

api.add_resource(resources.AddPatient, '/patient')
api.add_resource(resources.Patients, '/patient')
api.add_resource(resources.Patient, '/patient/<int:patient_id>')

if __name__ == '__main__':
    app.run(port=4000)
