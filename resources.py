from flask import request
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args

import models

class Patient(Resource):

    def get(self, patient_id):
        patientObject = models.get_patient(patient_id)
        if patientObject is None:
            return {'status': 404, 'message': 'Patient with id={} not found.'.format(patient_id)}
        return patientObject, 200

    def put(self, patient_id):
        if models.update_patient(patient_id, request.form):
            return patient_id, 200
        return {'status': 404, 'message': 'Patient with id={} not found.'.format(patient_id)}
    
    def delete(self, patient_id):
        if models.delete_patient(patient_id):
            return '', 200
        return {'status': 404, 'message': 'Patient with id={} not found.'.format(patient_id)}

class AddPatient(Resource):
    def post(self):
        data = request.form
        patient_id = models.create_patient(data)
        if patient_id is None:
            return {'status': 400, 'message': 'Insufficient Data'}
        return patient_id, 201

class Person(Resource):
    def get(self, person_id):
        personObject = models.get_person(person_id)
        if (personObject is None):
            return {'status': 404, 'message': 'Person with id={} not found.'.format(person_id)}
        return personObject, 200

class Persons(Resource):
    def get(self):
        persons = models.get_persons()
        return persons, 200

class Patients(Resource):
    patient_args = {
        'person_id': fields.Str(),
        'given_name': fields.Str(),
        'middle_name': fields.Str(),
        'family_name': fields.Str(),
        'city': fields.Str(),
        'provice': fields.Str(),
        'country': fields.Str(),
        'postal_code': fields.Str(),
        'identifier': fields.Str()
    }

    @use_args(patient_args)
    def get(self, args):
        patients = models.get_patients(args)
        return patients, 200
        