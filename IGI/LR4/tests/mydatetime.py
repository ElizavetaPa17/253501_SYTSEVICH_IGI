import datetime
import time
import calendar

# Максимально и минимально хранимые даты 
print(datetime.MAXYEAR, datetime.MINYEAR)

# Работа с timedelta
delta = datetime.timedelta(days = 1, weeks = 3, hours=11, minutes=20, seconds=11)
print(delta)
print(delta*2)
print(delta/2)
print(delta-delta)
print(delta.total_seconds())
print(delta.max, delta.min)
print(delta.resolution)

# Работа с date
my_date = datetime.date(2024, 3, 1)
print(my_date.today())
print(my_date+delta)
print(my_date.weekday())
print(my_date.ctime())

# Работа с calendar
cal = calendar.TextCalendar()
print(cal.formatmonth(my_date.year, my_date.month))