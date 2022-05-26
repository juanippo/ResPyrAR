#from datetime import datetime, date
#from dateutil.relativedelta import relativedelta

def daterange_d():
    print('Enter a initial date between  2018-06-28 and present, it must be in yyyy-mm-dd')
    while True:

        date_0=input('Start date: ')
        today=date.today()

        try:
          date_0o = datetime.strptime(date_0,'%Y-%m-%d').date()
        except ValueError:
           print("Put a valid date, it must be in yyyy-mm-dd.")
        else:         
           if date(2018,6,28) <= date_0o <= today:
                break
           else:
                print('The date that you enter is out of range, please input a date in between 2018-06-28 and',datetime.strftime(today,'%Y-%m-%d'))
    while True:     
        date_f=input('End date: ')
        try:
          date_fo = datetime.strptime(date_f,'%Y-%m-%d').date()
        except ValueError:
           print("Put a valid date, it must be in yyyy-mm-dd.")

        else:
           if date(2018,6,28) <= date_fo <= today: 
                if date_0o < date_fo:
                    break
                else:
                    print('The start date must be before the end date')
           else:
                print('The date that you enter is out of range, please input a date in between 2018-06-28 and',datetime.strftime(today,'%Y-%m-%d'))
    return(date_0o,date_0,date_fo,date_f)
    
def daterange_m():
    print('Enter a initial date between  2018-07 and present, it must be in yyyy-mm')
    while True:

        date_0=input('Start date: ')
        today=date.today()

        try:
          date_0o = datetime.strptime(date_0,'%Y-%m').date()
        except ValueError:
           print("Put a valid date, it must be in yyyy-mm")
        else:         
           if date(2018,6,28) <= date_0o <= today:
                break
           else:
                print('The date that you enter is out of range, please input a date in between 2018-07 and',datetime.strftime(today,'%Y-%m'))
    while True:     
        date_f=input('End date (this month will not be included): ')
        try:
          date_fo = datetime.strptime(date_f,'%Y-%m').date()
        except ValueError:
           print("Put a valid date, it must be in yyyy-mm.")

        else:
           if date(2018,6,28) <= date_fo <= today: 
                if date_0o < date_fo:
                    break
                else:
                    print('The start date must be before the end date')
           else:
                print('The date that you enter is out of range, please input a date in between 2018-07 and',datetime.strftime(today,'%Y-%m'))
    return(date_0o,date_0,date_fo,date_f)
    
def month_dateseries(I,F):
    I=datetime.strptime(I,'%Y-%m').date()
    F=datetime.strptime(F,'%Y-%m').date()
    r = relativedelta(F, I)
    Months=r.years*12+r.months
    date_generated = [I + relativedelta(months=x) for x in range(0, Months)]
    return (date_generated)
    
    
def selec_month_dataseries():
    date_I,date_Is,date_F,date_Fs = daterange_m()
    date_generated=month_dateseries(date_I,date_F)
    return(date_generated)
    
    
def selec_month_dataseries2(month_ini,month_end):
    date_generated=month_dateseries(month_ini,month_end)
    return(date_generated)