# utils code.
from password_strength import PasswordPolicy
import datetime

# setup the password policy.
policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=1,  # need min. 1 uppercase letter
    numbers=1,  # need min. 1 digit
    special=1,# need min. 1 special character
    nonletters=1,  # need min. 1 non-letter characters (digits, specials, anything)
)

# for checking password strength.
def check_password(password: str):
    # This returns true or False
    # if the test is empty([]), it means it matches with the password.
    return len(policy.test(password)) == 0

# exclude some fields while outputting
def remove_fields(data, fields):
    if isinstance(data, dict):
        for key in fields:
            data.pop(key, None)
        return {key: remove_fields(value, fields) for key, value in data.items()}
    elif isinstance(data, list):
        return [remove_fields(item, fields) for item in data]
    else:
        return data

def model_to_dict(data):
    data_types = (str, bool, int, datetime.datetime, dict, list, float)

    def convert_value(value):
        if not isinstance(value, data_types):
            return value.__dict__
        return value

    return {key: convert_value(value) for key, value in data.items()}
