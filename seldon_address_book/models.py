from seldon_address_book import db

class Organisation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    
    def __init__(self, name, address, phone):
        self.name = name
        self.address = address
        self.phone = phone

    def __repr__(self):
        return '<Organisation {}>'.format(self.name)

    
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    forename = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisation.id'))
    organisation = db.relationship('Organisation', backref=db.backref('persons', lazy='dynamic'))

    def __init__(self, forename, surname, organisation):
        self.forename = forename
        self.surname = surname
        self.organisation = organisation

    def __repr__(self):
        return '<Person {} {}>'.format(self.forename, self.surname)
