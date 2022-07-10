import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('mini_tax_calculator_sheet')

info = SHEET.worksheet('payee-data')

data = info.get_all_values()

print(data)

def welcome_message():
    """
    Dispay greetings, information about the application
    and instruction for the user.
    """
    print("\tWelcome to Mini Tax Calculator.\n")
    print("This application will help You qickly calculate your taxes")
    print("The application needs to ask you for few informations that are necessary for calculate your taxes")
    print("All sensitive data are to be used for the calculations purposes only, and will never be shared")
    print("or used for any other purpose.\n")


def get_user_name():
    """
    Display asking for the users name.
    Returns that name.
    """
    name = validate_name(input("Please enter your name here: \n"))
    print(f"Welcome {name} Thank You for using our application")
    return name

def validate_name(name):
    """
    Validate input data
    Check if the name doesn't contain other than
    letters. Accepted are only upper and lowercase letters.
    """
    if name.replace(" ", "").isalpha():
        print ("Name is valid!")
        return name
    else:
        print ("Name is invalid! Use letters from A to Z or a to z.")
        return validate_name(input("Please enter your name again \n"))


def quit_all():
    """
    This function is called when Q-key is pressed on the keyboard 
    it interrupts the whole process and 
    moves the user to the welcome_message function where he can 
    start the application from the beginning.
    """
    print("Are you sure you want to quit the process?")
    while True:
        confirm = input('Press "Y" to quit or "N" to return\n')
        if confirm.upper() == "Y":
            print("Process interrupted by the user\n\n")
            create_person()
            break
        elif confirm.upper() == "N":
            print("Return to the process\n")
            break
        else:
            print('Tap "Y" to submit or "N" to return to the previous process')


def request_salary():
    """
    Request salary from the user. 
    The entered value has to be validated for being integer and 
    having the right format.
    If the user doesn't know the value of his salary it can be 
    calculated after typing C-key on keyboard.
    """
    print("\nWe need your weekly salary to calculate your taxes.")
    print('Please enter your salary in following format: 99.99 ')
    while True:
        print('Please enter your weekly salary or type "C" to calculate it.')
        user_input = input('If you want to quit You can press "Q". \n')
        if user_input.upper() == "Q":  
            quit_all()
        elif user_input.upper() == "C":
            calculate_salary()
            break
        elif validate_salary(user_input):
            print(f"Your salary is {user_input}")
            return user_input
            break

def calculate_salary():
    """
    Calculate salary based on multiplication of weekly working hours and
    hourly rate.
    Hourly rate can be validated using validate_salary.
    Working hours must be validated especially dedicated function..
    """
    salary = 0
    try:
        hourly_rate = float(input("Enter your rate per hour\n"))
        working_hours = float(input("Enter your weekly working hours\n"))

        salary = "{:.2f}".format(hourly_rate * working_hours)
        print(f"You work {working_hours} hours for {hourly_rate}/hour. Nice!")
        print(f'You earn {salary} quid')
    except ValueError as e:
        print(f"Invalid data: {e}, please try again. \n")
        calculate_salary()

    return salary


def validate_salary(salary):
    """
    Check if input salary data is an integer or float type,
    and it is entered in the right format
    The function returns validated salary value.

    The function rounds the value to the demanded format instead of checking its
    correctness.
    """
    try:
        # Line below doesn't make a sense. The function returns Boolean.
        "{:.2f}".format(float(salary))
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    print(f"Your salary {salary} was successfully validated ")
    return True
        

def get_age():
    """
    Get age data from the user.
    Validate the data if it is the int type data.
    """
    age = 0
    try:
        age = input("Enter your age or choose Q to quit\n")
        if age == "Q" or age == "q":
            quit_all()
            raise IndexError
        else:
            age = int(age)
            print(f'You are {age} years old')
    except ValueError as e:
        print(f"Invalid data: {e}, please try again. \n")
        age = get_age()
    return age

def is_in_relation():
    """
    Get information about formal relation from the user.
    Any input that is a string that starts with the first character "n" or "N"
    will be recognized as Yes.
    Also any input that starts with "N" or "n" will be recognized as No.
    "Q" or "q" input will launch quit_all function that interrupts the process.
    """
    print("Are you living in a formal relation?")
    relation = input('Press "Y" for Yes or "N" if you are not or choose Q to quit.\n')
    if relation[0] == "Y" or relation[0] == "y":
        print("You are in relation")
        return True
    elif relation[0] == "N" or relation[0] == "n":
        print("You are not in a relation")
        return False
    elif relation == "Q" or relation == "q":
        quit_all()
    else:
        print("Invalid value. Please try again")
        is_in_relation()

class Person:
    """
    Store users data; such as name, age, information about formal relations and 
    users salary.
    These data are base to further calculations 
    """
    def __init__(self, name, age, relation, salary):
        self.name = name
        self.age = age
        self.relation = relation
        self.salary = salary
    

def create_person():
    """
    An unfixed bug. Quit option inside each of data request functions interrupt only
    the functions they are in, but they don't interrupt create_person function.
    After the function is quit create_person function is resumed.
    """
    name = get_user_name()
    salary = request_salary()
    age = get_age()
    relation = is_in_relation()
    person = Person(name, age, relation, salary)
    print(f'{person.name} - {person.age} years old. Married: {person.relation}, Salary - {person.salary}')


def main():
    welcome_message()
    create_person()
    print("Thank you for filling in the form. Now we are going to process your data")

main()
