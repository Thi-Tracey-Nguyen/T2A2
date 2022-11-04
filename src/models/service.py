from init import db, ma

class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)

    bookings = db.relationship('Booking', back_populates = 'service')

class ServiceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'duration', 'price', 'bookings')
        ordered = True