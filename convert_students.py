# Rename check_in_out.txt to borrowed_log.txt


# This code converts the old student.txt file into the new format.
# This new format allows the first name, last name, and period number
# to be taken out without assumtions for it's use, before it assumed
# that it would be accesed for a welcome message. now it can be changed
# easier. This puts the result into "converted_students.txt," which
# should replace "students.txt," but doesn't automatically override
# students.txt because of potential errors.
# Once converted_students.txt has been vetted, it should replace students.txt
# and this script can be deleted

# Open the students.text file and read it.
with open("./students.txt", "r") as inf:
    students = eval(inf.read()) # set the contents to a variable students
    converted_students = {}

    for qrid, student in students.items():
        # The variable student should be formatted as "first_name last_name, period period_number," with the trailing comma optional

        # student.split(' ') Splits student by it's spaces to look like ["first_name", "last_name,", "period", "period_number,"]
        # ...[:2] Then take only the first two items, ["first_name", "last_name,"] and split them into variables first_name and last_name respectively
        first_name, last_name = student.split(' ')[:2]
        
        last_name = last_name[:-1] # Removes the added comma in last_name
        
        # student.split('period ') Split students to look like ["first_name last_name,", "period_number,"]
        # ...[1] take the second item(python is 0-indexed)
        # ...[:1] take only the first character
        period = student.split('period ')[1][:1]
        
        # The new format
        student = {
            "first_name": first_name,
            "last_name": last_name,
            "period": period
        }
        converted_students[qrid] = student
    
    f = open("./converted_students.txt", "w+")
    f.write(str(converted_students))
    f.close()