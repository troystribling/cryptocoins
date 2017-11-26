from datetime import timedelta


def day_dir(file_date):
    return file_date.strftime('%Y%m%d')


def date_prefix(file_date):
    return file_date.strftime('%Y%m%d-%H%M%S-')


def daterange(date1, date2):
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + timedelta(n)

def valid_params(expected_params, params):
    for expected_param in expected_params:
        if expected_param not in params:
            print(f"ERROR: '{expected_param}' KEY IS MISSING FROM {params}")
            return False
    return True
