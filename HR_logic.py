from PyQt6.QtWidgets import *
from HR_home import *
import csv
import pandas as pd

"""dictionary of positions at company"""
positions = {"manager": 40, "engineer": 30, "analyst": 25, "intern": 10}


def employee_check(first, last, employee_id) -> None:
    """checks if employee is valid in csv sheet by looking at the inputted first name, last name,
    and employee ID. Will raise an error if employee isn't found"""
    val = False
    with open('Tech_co.csv', 'r') as file:
        csvfile = csv.reader(file)
        for line in csvfile:
            if line[0].lower() == first.lower() and line[1].lower() == last.lower() and line[2] == employee_id:
                val = True
    if val is False:
        raise ValueError
    else:
        pass


def pay_method(first, last, employee_id, hours) -> str:
    """validates employee in csv file and will calculate their payment and return a formatted string as variable
    'message.' If message stays blanks, an error will be raised"""
    message = ''
    with open('Tech_co.csv', 'r') as file:
        csvfile = csv.reader(file)
        for line in csvfile:
            if line[0].lower() == first.lower() and line[1].lower() == last.lower() and line[2] == employee_id:
                payment = float(float(hours) * int(line[4]))
                message = (f"Employee {first} {last} (ID: {employee_id}) was paid ${payment:.2f} "
                           f"for {hours} hours of work ")
                return message
    if message == '':
        raise ValueError
    else:
        return message


def check_all_ids(ID) -> None:
    """reads through csv file to make list of all employee IDs. checks if inputted ID is inside the list all IDs.
    Will raise an error if a repeated ID is found."""
    all_emp_ids = []
    with open('Tech_co.csv', 'r') as file:
        csvfile = csv.reader(file)
        for line in csvfile:
            all_emp_ids.append(line[2])
    for i in all_emp_ids:
        if i == ID:
            raise ValueError
        else:
            pass


def check_position(input_position) -> (str, int):
    """accesses the position dictionary and grab the pay rate of the position noted, raises an error if position
    given is not found"""
    current_pos = ''
    for i in positions:
        if i.lower() == input_position.lower():
            current_pos = i
            return current_pos, positions.get(current_pos)
    if current_pos == '':
        raise ValueError


class MainLogic(QMainWindow, Ui_Form):
    def __init__(self) -> None:
        """Set up for creating the main window"""
        super().__init__()
        self.setupUi(self)
        self.stackedWidget.setCurrentWidget(self.pay_page)

        """Connect the side buttons to the functions that move between pages"""
        self.hire_action.clicked.connect(lambda: self.go_hire_page())
        self.fire_action.clicked.connect(lambda: self.go_fire_page())
        self.pay_action.clicked.connect(lambda: self.go_pay_page())

        """Connect the submit buttons of each page to their respective functions"""
        self.hire_submit.clicked.connect(lambda: self.hire_person())
        self.pay_submit.clicked.connect(lambda: self.pay_person())
        self.fire_submit.clicked.connect(lambda: self.delete_person())

    """The following functions are created to jump around the 3 different pages and clears the previous one of inputs"""
    def go_hire_page(self) -> None:
        self.stackedWidget.setCurrentWidget(self.hire_page)
        self.clear()

    def go_fire_page(self) -> None:
        self.stackedWidget.setCurrentWidget(self.fire_page)
        self.clear()

    def go_pay_page(self) -> None:
        self.stackedWidget.setCurrentWidget(self.pay_page)
        self.clear()

    """functions that clears all pages of inputs"""
    def clear(self) -> None:
        """clear the inputs and bottem text of pay page"""
        self.first_name.clear()
        self.last_name.clear()
        self.hour.clear()
        self.employee_id.clear()
        self.pay_details.setText("")
        """clear the inputs and bottom text of hire page"""
        self.first_name_2.clear()
        self.last_name2.clear()
        self.employee_ID2.clear()
        self.new_position.clear()
        self.label_4.setText("")
        """clear the inputs and bottom text of fire page"""
        self.first_name3.clear()
        self.last_name3.clear()
        self.employee_ID3.clear()
        self.label_5.setText('')

    def hire_person(self) -> None:
        """function will get information from gui and see if the new employee's ID already exists and if the position is
        also valid. If no error is raised, then the employee is added to csv file"""
        first = self.first_name_2.text()
        last = self.last_name2.text()
        new_id = self.employee_ID2.text()
        input_position = self.new_position.text()
        first = str(first)
        last = str(last)
        try:
            check_all_ids(new_id)
            position, rate = check_position(input_position)
        except ValueError:
            self.label_4.setText("Employee ID already Exists or invalid inputs")
        else:
            self.label_4.setText(f"New employee {first} {last} (ID: {new_id}) is HIRED!")
            with open("Tech_co.csv", 'a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['FirstName', 'LastName', 'ID', 'Position', 'Rate'])
                writer.writerow({'FirstName': first, 'LastName': last, 'ID': new_id,
                                 'Position': position, 'Rate': rate})

    def pay_person(self) -> None:
        """Will get information from gui and use pay_method to show a message if no error is raised. Error is
        raised if pay_method raised one"""
        try:
            first = self.first_name.text().lower()
            last = self.last_name.text().lower()
            employee_id = self.employee_id.text()
            hour = self.hour.text()
            payment = pay_method(first, last, employee_id, hour)
            self.pay_details.setText(payment)
        except ValueError:
            self.pay_details.setText(f"Employee does not exist or invalid inputs")

    def delete_person(self) -> None:
        """Will get information from gui and use employee_check function validate if employee exists. Uses Pandas module
        to delete the employee from csv if validated. Error is raised if employee could not be found."""
        first = self.first_name3.text()
        last = self.last_name3.text()
        id_employee = self.employee_ID3.text()
        try:
            employee_check(first, last, id_employee)
            df = pd.read_csv('Tech_co.csv')
            df = df.drop(df[df.ID == str(id_employee)].index)
            df.to_csv('Tech_co.csv', index=False)
        except ValueError:
            self.label_5.setText(f"Employee {id_employee} could not find or invalid name")
        else:
            self.label_5.setText(f"Employee {id_employee} is fired!")
