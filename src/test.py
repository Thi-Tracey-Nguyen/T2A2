from datetime import datetime, date

def validate_date(date):
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    if date_obj < date.today():
        print('Booking date must be in the future')

print(date.today())
print(datetime.strptime('2022-11-04', '%Y-%m-%d').date())
print(datetime.strptime('09:00', '%H:%M').time())
print(datetime.now().time())
