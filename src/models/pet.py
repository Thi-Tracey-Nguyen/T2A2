# from init import db, ma 
# from marshmallow import fields

# class Pet(db.Model):
#     __tablename__ = 'pets'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(15), nullable=False)
#     type = db.Column(db.String(10), nullable=False)
#     size = db.Column(db.String, nullable=False)
#     breed = db.Column(db.String(50))

#     client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))

#     client = db.relationship('Client', back_populates = ['pet'])

# class PetSchema(ma.Schema):
#     client = fields.Nested('ClientSchema', only = ['f_name', 'l_name', 'phone'])

#     class Meta:
#         fields = ('id', 'name', 'type', 'size', 'breed', 'client')
#         ordered = True