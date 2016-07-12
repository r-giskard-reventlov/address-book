from flask import request, jsonify
from seldon_address_book import app, db
from seldon_address_book.models import Organisation, Person

@app.route('/', methods=['GET'])
def discover():
    response = jsonify({
        "links": [{
            "rel": "create-organisation",
            "href": "/organisations"
        }]
    })
    response.status_code = 200
    return response

@app.route('/organisations', methods=['POST'])
def create_organisation():
    payload = request.get_json()
    organisation = _create_organisation(payload)
    db.session.add(organisation)
    db.session.commit()
    response = jsonify({
        "links": [
            {
                "rel": str(organisation.id),
                "href": "/organisations/" + str(organisation.id)
            },
            {
                "rel": "add-person",
                "href": "/organisations/" + str(organisation.id) + "/persons"
            }
        ]
    })
    response.status_code = 201
    response.headers['location'] = '/organisations/' + str(organisation.id)
    return response

@app.route('/organisations/<int:organisation_id>', methods=['GET'])
def retrieve_organisation(organisation_id):
    organisation = Organisation.query.get(organisation_id)
    response = jsonify(organisation.serialise())
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
        "links": [
            {
                "rel": str(person.id),
                "href": "/organisations/" + str(organisation_id) + "/persons/" + str(person.id)
            }
        ]
    })
    response.status_code = 201
    response.headers['location'] = "/organisations/" + str(organisation_id) + "/persons/" + str(person.id)
    return response    


def _create_person(payload):
    return Person(payload['forename'], payload['surname'])

def _create_organisation(payload):
    return Organisation(payload['name'], payload['address'], payload['phone'])
