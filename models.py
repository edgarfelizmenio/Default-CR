import uuid

from database import Base, db_session

Person = Base.classes.Person
PersonName = Base.classes.PersonName
PersonAddress = Base.classes.PersonAddress
PersonAttribute = Base.classes.PersonAttribute
PersonAttributeType = Base.classes.PersonAttributeType
Patient = Base.classes.Patient
PatientIdentifier = Base.classes.PatientIdentifier
PatientIdentifierType = Base.classes.PatientIdentifierType

patient_classes = {
    'person_id': Person,
    'given_name': PersonName,
    'middle_name': PersonName,
    'family_name': PersonName,
    'city': PersonAddress,
    'provice': PersonAddress,
    'country': PersonAddress,
    'postal_code': PersonAddress,
    'identifier': PatientIdentifier
}

def get_persons():
    result = db_session.query(Person.person_id)
    return [person.person_id for person in result]

def get_patients(args):
    if len(args) > 0:
        query = db_session.query(Person,
                                 PersonName,
                                 PersonAddress,
                                 Patient,
                                 PatientIdentifier,
                                 PatientIdentifierType).join(
                                     PersonName).join(
                                         PersonAddress).join(
                                             Patient).join(
                                                 PatientIdentifier).join(
                                                     PatientIdentifierType)
        for k, v in args.items():
            query = query.filter(getattr(patient_classes[k], k).like('%{}%'.format(v)))
            result = query.all()
            if result is None:
                return None
            return [extract_patient_object(r) for r in result]
    else:
        result = [patient.patient_id for patient in db_session.query(Patient.patient_id)]
    return result


def get_person(person_id):
    result = db_session.query(Person, PersonName, PersonAddress).join(
        PersonName).join(
            PersonAddress).filter(Person.person_id == person_id).first()
    if result is None:
        return None
    (person, person_name, person_address) = result
    person_object = {
        "person_id": person.person_id,
        "given_name": person_name.given_name,
        "middle_name": person_name.middle_name,
        "family_name": person_name.family_name,
        "gender": person.gender,
        "address1": person_address.address1,
        "address2": person_address.address2,
        "city": person_address.city_village,
        "province": person_address.state_province,
        "country": person_address.country,
        "postal_code": person_address.postal_code
    }
    attributes = []
    attr_result = db_session.query(PersonAttribute, PersonAttributeType).join(
        PersonAttributeType
    ).filter(PersonAttribute.person_id == person_object["person_id"]).all()
    for person_attribute, person_attribute_type in attr_result:
        attributes.append({
            "name": person_attribute_type.name,
            "description": person_attribute_type.description,
            "format": person_attribute_type.format,
            "value": person_attribute.value
        })
    person_object["attributes"] = attributes
    return person_object

def get_patient(patient_id):
    result = db_session.query(Person,
                              PersonName,
                              PersonAddress,
                              Patient,
                              PatientIdentifier,
                              PatientIdentifierType).join(
                                  PersonName).join(
                                      PersonAddress).join(
                                          Patient).join(
                                              PatientIdentifier).join(
                                                  PatientIdentifierType).filter(
                                                      Patient.patient_id == patient_id).first()
    if result is None:
        return None
    return extract_patient_object(result)

def create_patient(data):
    if 'given_name' not in data or 'family_name' not in data:
        return None
    person = Person(gender=data.get('gender', None))
    person_name = PersonName(person=person,
        given_name = data.get('given_name', None),
        middle_name = data.get('middle_name', None),
        family_name = data.get('family_name', None),
        uuid = str(uuid.uuid4()))
    person_address = PersonAddress(person=person,
        address1 = data.get('address1', None),
        address2 = data.get('address2', None),
        city_village = data.get('city', None),
        state_province = data.get('province', None),
        country = data.get('country', None),
        postal_code = data.get('postal_code', None))
    db_session.add(person)
    db_session.add(person_name)
    db_session.add(person_address)
        
    db_session.flush()

    patient = Patient(person=person)
    patient_identifier = PatientIdentifier(patient=patient,
        identifier_type = 2,
        identifier = '{}_{}_{}'.format(person.person_id, 
            data.get('given_name',''), 
            data.get('family_name','')))
    
    db_session.add(patient)
    db_session.add(patient_identifier)
    db_session.commit()
    return patient.patient_id

def update_patient(patient_id, data):
    result = db_session.query(Person,
                              PersonName,
                              PersonAddress,
                              Patient,
                              PatientIdentifier,
                              PatientIdentifierType).join(
                                  PersonName).join(
                                      PersonAddress).join(
                                          Patient).join(
                                              PatientIdentifier).join(
                                                  PatientIdentifierType).filter(
                                                      Patient.patient_id == patient_id).first()
    if result is None:
        return None
    (person, person_name, person_address, patient, patient_identifier, patient_identifier_type) = result
    person.gender = data.get('gender', person.gender)
    person_name.given_name = data.get('given_name', person_name.given_name)
    person_name.middle_name = data.get('middle_name', person_name.middle_name)
    person_name.family_name = data.get('family_name', person_name.family_name)
    person_address.city_village = data.get('city', person_address.city_village)
    person_address.state_province = data.get('province', person_address.state_province)
    person_address.country = data.get('country', person_address.country)
    person_address.postal_code = data.get('postal_code', person_address.postal_code)
    if 'given_name' in data or 'family_name' in data:
        patient_identifier.identifier = '{}_{}_{}'.format(person.person_id, data.get('given_name', person_name.given_name), data.get('family_name', person_name.family_name))
    db_session.commit()
    return extract_patient_object(result)


def delete_patient(patient_id):
    result = db_session.query(Patient, PatientIdentifier).join(
                    PatientIdentifier).filter(Patient.patient_id == patient_id).first()
    if result is not None:
        (patient, patient_identifier) = result 
        db_session.delete(patient)
        db_session.delete(patient_identifier)
        db_session.commit()
        return True
    return False

def extract_patient_object(row):
    (person, person_name, person_address, patient, patient_identifier, patient_identifier_type) = row
    patient_object = {
        "person_id": person.person_id,
        "given_name": person_name.given_name,
        "middle_name": person_name.middle_name,
        "family_name": person_name.family_name,
        "uuid": person_name.uuid,
        "gender": person.gender,
        "address1": person_address.address1,
        "address2": person_address.address2,
        "city": person_address.city_village,
        "province": person_address.state_province,
        "country": person_address.country,
        "postal_code": person_address.postal_code,
        "identifier": patient_identifier.identifier,
        "identifier_type": patient_identifier_type.name,
        "identifier_type_description": patient_identifier_type.description,
        "location_id": patient_identifier.location_id
    }
    attributes = []
    attr_result = db_session.query(PersonAttribute, 
                                PersonAttributeType).join(
                                PersonAttributeType
    ).filter(PersonAttribute.person_id == patient_object["person_id"]).all()
    for person_attribute, person_attribute_type in attr_result:
        attributes.append({
            "name": person_attribute_type.name,
            "description": person_attribute_type.description,
            "format": person_attribute_type.format,
            "value": person_attribute.value
        })
    patient_object["attributes"] = attributes
    return patient_object