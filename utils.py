# utils code.
from password_strength import PasswordPolicy

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