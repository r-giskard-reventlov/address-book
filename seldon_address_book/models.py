from seldon_address_book import db


class Organisation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    persons = db.relationship('Person')
    
    def __init__(self, name, address, phone):
        self.name = name
        self.address = address
        self.phone = phone

    def serialise(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
            "persons": [p.serialise() for p in self.persons]
        }

    def __repr__(self):
        return '<Organisation {}>'.format(self.name)

    
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    forename = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisation.id'))

    def __init__(self, forename, surname):
        self.forename = forename
        self.surname = surname

    def serialise(self):
        # TODO : add in self link to person, id should be a url to the person
        return {
            "id": self.id,
            "forename": self.forename,
            "surname": self.surname
        }

    def __repr__(self):
        return '<Person {} {}>'.format(self.forename, self.surname)
