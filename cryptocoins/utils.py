from datetime import timedelta


def day_dir(file_date):
    return file_date.strftime('%Y%m%d')


def date_prefix(file_date):
    return file_date.strftime('%Y%m%d-%H%M%S-')


def daterange(date1, date2):
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + timedelta(n)
