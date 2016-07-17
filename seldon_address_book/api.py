from flask import request, jsonify
from seldon_address_book import app, db
from seldon_address_book.models import Organisation, Person

# TODO : move into config
HOST = 'http://localhost:8080'

@app.route('/', methods=['GET'])
def discover():
    response = jsonify({
        'links': [
            {
                'rel': 'self',
                'href': HOST
            },
            {
                'rel': 'organisations',
                'href': HOST + '/organisations'
            }
        ]
    })
    response.status_code = 200
    return response

@app.route('/organisations', methods=['GET'])
def retrieve_organisations():
    organisations = Organisation.query.all()
    organisations_array = [o.serialise() for o in organisations];
    organisations_with_links = _organisations_with_links(organisations_array)
    response = jsonify({
        'organisations' : organisations_with_links,
        'links': [
            {
                'rel': 'self',
                'href': HOST + '/organisations'
            }
        ]
    })
    response.status_code = 200
    return response

@app.route('/organisations', methods=['POST'])
def create_organisation():
    payload = request.get_json()
    organisation = _create_organisation(payload)
    db.session.add(organisation)
    db.session.commit()
    response = jsonify({})
    response.status_code = 201
    response.headers['location'] = HOST + '/organisations/' + str(organisation.id)
    return response

@app.route('/organisations/<int:organisation_id>', methods=['GET'])
def retrieve_organisation(organisation_id):
    organisation = Organisation.query.get(organisation_id)
    response = jsonify({
        'organisation': organisation.serialise(),
        'links': [
            {
                'rel': 'self',
                'href': HOST + '/organisations/' + str(organisation_id)
            }
        ]
    })
    response.status_code = 200
    return response

@app.route('/organisations/<int:organisation_id>', methods=['DELETE'])
def delete_organisation(organisation_id):
    organisation = Organisation.query.get(organisation_id)
    db.session.delete(organisation)
    db.session.commit()
    response = jsonify({})
    response.status_code = 204
    return response

@app.route('/organisations/<int:organisation_id>', methods=['PUT'])
def update_organisation(organisation_id):
    organisation = Organisation.query.get(organisation_id)
    payload = request.get_json();
    print(payload);
    organisation.name = payload['name']
    organisation.address = payload['address']
    organisation.phone = payload['phone']
    organisation.persons = _persons_from(payload['persons'])
    db.session.commit()
    response = jsonify({'organisation': organisation.serialise()})
    response.status_code = 200
    return response

@app.route('/organisations/<int:organisation_id>/persons', methods=['POST'])
def create_person(organisation_id):
    payload = request.get_json()
    person = _create_person(payload)
    organisation = Organisation.query.get(organisation_id)
    organisation.persons.append(person)
    db.session.add(person)
    db.session.add(organisation)
    db.session.commit()
    response = jsonify({
        'links': [
            {
                'rel': str(person.id),
                'href': '/organisations/' + str(organisation_id) + '/persons/' + str(person.id)
            }
        ]
    })
    response.status_code = 201
    response.headers['location'] = '/organisations/' + str(organisation_id) + '/persons/' + str(person.id)
    return response    


def _organisations_with_links(organisations):
    return [_add_link(o) for o in organisations]

def _add_link(organisation):
    organisation['id'] = {
        'rel': 'self',
        'href': HOST + '/organisations/' + str(organisation['id'])
    }
    return organisation
    
def _persons_from(persons):
    return [Person(p['forename'], p['surname']) for p in persons]

def _create_person(payload):
    return Person(payload['forename'], payload['surname'])

def _create_organisation(payload):
    return Organisation(payload['name'], payload['address'], payload['phone'])
