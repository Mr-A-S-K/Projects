import re

def check_password_strength(password):
    # Minimum length requirement
    min_length = 8
    
    # Regular expressions for complexity requirements
    contains_lowercase = re.compile(r'[a-z]')
    contains_uppercase = re.compile(r'[A-Z]')
    contains_digit = re.compile(r'\d')
    contains_special_char = re.compile(r'[!@#$%^&*(),.?":{}|<>]')

    # Check minimum length
    if len(password) < min_length:
        return "Weak: Password should have at least {} characters.".format(min_length)

    # Check for lowercase, uppercase, digits, and special characters
    requirements = [contains_lowercase, contains_uppercase, contains_digit, contains_special_char]
    unsatisfied_requirements = [req for req in requirements if not req.search(password)]

    if unsatisfied_requirements:
        return "Weak: Password should include {}.".format(', '.join([req.pattern for req in unsatisfied_requirements]))
    
    return "Strong: Password meets the complexity requirements."

# Ask for a password until it meets the requirements
while True:
    user_password = input("Enter your password: ")
    result = check_password_strength(user_password)
    print(result)
    
    if "Strong" in result:
        break  # Exit the loop if the password is strong
