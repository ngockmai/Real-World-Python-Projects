grades = {
    "Alice": 78,
    "Bob" : 43,
    "Charlie" : 65,
    "Diana" : 49,
    "Eve": 90
}

#Create a new dictionary with "Pass" and "Fail" based on their grades
results = {}
for student, grade in grades.items():
    if grade >= 50:
        results[student] = "Pass"
    else:
        results[student] = "Fail"

#Iterate through the results dictionary and print the student and their result
print("Student Categories:")
for student, result in results.items():
    print(f"{student}: {result}")