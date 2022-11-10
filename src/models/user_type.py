from init import db, ma
from marshmallow import fields, validates
from marshmallow.exceptions import ValidationError

class UserType(db.Model):
    __tablename__ = 'user_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))

    users = db.relationship('User', back_populates = 'type', cascade='all, delete')

class UserTypeSchema(ma.Schema):
    users = fields.List(fields.Nested('UserSchema', exclude=['type']))

    @validates('name')
    def validate_name(self, value):
        if len(value) < 2:
            raise ValidationError('Type name must be longer than 2 characters')
            
        stmt = db.select(UserType).filter_by(name = value.capitalize())
        type_name = db.session.scalar(stmt)

        if type_name:
            raise ValidationError('User type already exists')
            
    class Meta:
        fields = ('id', 'name', 'users')
        ordered = True