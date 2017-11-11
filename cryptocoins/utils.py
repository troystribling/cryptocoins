from datetime import date, datetime

def day_dir(file_date):
    return file_date.strftime('%Y%m%d')

def date_prefix(file_date):
    return file_date.strftime('%Y%m%d-%H%M%S-')
