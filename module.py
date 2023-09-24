import datetime, bday

date1 = datetime.date.today()

birthday_date = datetime.date(1998, 2, 16)

days_until_birthday = date1 - birthday_date



if birthday_date == date1:
    print(bday.birthday_messages)
else:
    print(days_until_birthday)
    print(bday.birthday_messages)
