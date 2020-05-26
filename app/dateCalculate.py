from time import strftime, localtime
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import calendar

def month_offset(start_date, number_of_month):
    return datetime.strptime(start_date, '%Y-%m-%d') + relativedelta(months=number_of_month)

# print(get_today_month(-3))
print(month_offset('2019-01-31', 1))
