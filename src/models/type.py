from init import db, ma

class Type(db.Model):
    __tablename__ = 'types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))

    pet = db.relationship('Pet', back_populates = 'type')

class TypeSchema(ma.Schema):
    fields = ('id', 'name')
    ordered = True