
from datetime import datetime
from uuid import uuid4

def get_curr_datetime_str():
    now = datetime.now()
    return f"{now.year}{now.month}{now.day}T{now.hour}{now.minute}{now.second}"

def gen_shortened_uuid():
    return str(uuid4())[0:6]

def gen_log_file_name():
    return get_curr_datetime_str() + "_" + gen_shortened_uuid() + "_log.txt"