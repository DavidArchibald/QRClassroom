#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This script is made to convert the format of the student.json information.

To use it, run on a command line:
    $ python convert_students.py

If it runs smoothly, and converts correctly, the following doesn't apply.
Todo:
    * Be used on the the real database.
    * Fix any unknown issues that could arise.

Explanation:
    This new format allows the first name, last name, and period number
    to be taken out without assumtions for it's use. Before it assumed
    that it would be accesed for a welcome message. Now it can be changed
    easier.

Effect:
    This puts the result into the file "converted_students.json", once
    converted_students.json has been vetted, it should be renamed students.json
    and then students.txt and this script can be deleted.
"""

import ast # Enables safe conversion of a text file to a valid datatype in python.
import json # Reading and writing of json files.
import os.path

def main():
    """Converts the format of students.txt"""
    students = get_students()
    converted_students = {}

    for qrid, student in students.items():
        # "student" should be formatted as "first_name last_name, period period_number,"

        # Splits student to look like ["first_name", "last_name,", "period", "period_number,"]
        # And then unpacks them into their respective variables, discarding the rest .
        first_name, last_name, *_ = student.split(' ')

        last_name = last_name[:-1] # Removes the added comma in last_name

        # Splits the student to look like ["first_name last_name,", "period_number,"].
        # Then takes the period number by taking the second item's first character.
        period = student.split('period ')[1][:1]

        student = {
            "first_name": first_name,
            "last_name": last_name,
            "period": period
        }
        converted_students[qrid] = student

    set_converted_students(json.dumps(converted_students))

def get_students():
    """Get the student"""
    students_path ="./students.json"
    if not os.path.exists(students_path):
        students = []
        with open(students_path, "w+") as f:
            f.write(students)
            return students

    with open(students_path, "r") as inf:
        students = ast.literal_eval(inf.read()) # Read the contents of the file safely.
        return students

def set_converted_students(students):
    """Set the converted_students.json file's contents.
    
    Arguments:
        students {Any} -- The new contents of the file.
    """
    file = open("./converted_students.json", "w+")
    file.write(students)
    file.close()


if __name__ == '__main__':
    main()
