# Exercise 10-2: Learning C

# Open the file and read each line
with open('learning_python.txt') as file_object:
    lines = file_object.readlines()

# Loop through each line, replace "Python" with "C", and print it
for line in lines:
    modified_line = line.replace('Python', 'C')
    print(modified_line.strip())