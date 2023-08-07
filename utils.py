# utils code.
from password_strength import PasswordPolicy
import datetime
import re
from db.user_model import ClientUsers

# setup the password policy.
policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=1,  # need min. 1 uppercase letter
    numbers=1,  # need min. 1 digit
    special=1,# need min. 1 special character
    nonletters=1,  # need min. 1 non-letter characters (digits, specials, anything)
)

# check if the password is an email or not.
def is_password_email(password):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, password) is not None

# for checking password strength.
def check_password(password: str,  username: str = "", user: ClientUsers = None):
    # This returns true or False with the error message.
    error_message = []
    check = True
    pass_check = policy.test(password)
    pass_check = [str(e) for e in pass_check]
    
    if "Length(8)" in pass_check:
        error_message.append("\nPassword must be at least 8 characters long")
        check = False
        
    if "Uppercase(1)" in pass_check:
        error_message.append("\nPassword must include atleast 1 Uppercase character")
        check = False
        
    if "Numbers(1)" in pass_check:
        error_message.append("\nPassword must include atleast 1 Number")
        check = False
        
    if "Special(1)" in pass_check:
        error_message.append("\nPassword must include atleast 1 Special case character")
        check = False
        
    if "Nonletter(1)" in pass_check:
        error_message.append("\nPassword must include atleast 1 Non Character")
        check = False
        
    if not any(char.islower() for char in password):
        error_message.append("\nPassword must include atleast 1 Lowercase Character")
        check = False
    
    if is_password_email(password):
        error_message.append("\nPassword should not be an email address")
        check = False
        
    if user is not None and password.lower() == user.username.lower():
        error_message.append("\nYour Password cannot be your username")
        check = False
    
    if username != "" and password.lower() == username.lower():
        error_message.append("\nYour Password cannot be your username")
        check = False
        
    return check, ".".join(error_message)
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

# This function gets the user from the decoded access token.
def get_active_user(db, payload: dict):
    username = payload.get("sub")
    client_id = payload.get("client_id")
    
    return ClientUsers.check_client_username(
        db, client_id, username)