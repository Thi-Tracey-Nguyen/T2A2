from init import db, ma
from datetime import datetime
from models.employee import Employee
from marshmallow import fields, validates, validates_schema
from marshmallow.exceptions import ValidationError

class Roster(db.Model):
    __tablename__ = 'rosters'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'),
     nullable=False)

    employee = db.relationship('Employee')

class RosterSchema(ma.Schema):
    employee = fields.Nested('EmployeeSchema', only = ['user'])

    #validate that input date is valid and follows 'YYYY-MM-DD' format
    @validates('date')
    def validate_date(self, date):
        try:
            date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            raise ValidationError("Input date is invalid or does not conform to 'YYYY-MM-DD' format")

    #validate employee_id
    @validates('employee_id')
    def validate_employee_id(self, employee_id):
        stmt = db.select(Employee).filter_by(id = employee_id)
        employee = db.session.scalar(stmt)

        if not employee:
            raise ValidationError('Employee id does not exist')

    #ensure one employee can't be double-rostered for the same date
    @validates_schema
    def validate_employee_date(self, data, **kwargs):
        
        #retrieve a roster where employee_id and date match input data
        stmt = db.select(Roster).where(db.and_(
            Roster.employee_id == data['employee_id'], Roster.date == data['date']))
        roster = db.session.scalar(stmt)

        #if such roster exists, raise an exception
        if roster:
            raise ValidationError('Employee is already rostered for this date')

    class Meta:
        fields = ('id', 'date', 'employee', 'employee_id')
        ordered = True