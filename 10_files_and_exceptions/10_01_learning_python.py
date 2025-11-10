# In Python you can store data in variables.
# In Python you can write loops to repeat actions.
# In Python you can define functions to organize your code.
# In Python you can use classes to model real-world objects.

# Exercise 10-1: Learning Python

# First, read the entire file and print its contents
print("📘 Reading the entire file:\n")

with open('learning_python.txt') as file_object:
    contents = file_object.read()
    print(contents)

# Second, read the file line by line and print each line using a loop
print("\n📘 Reading the file line by line:\n")

with open('learning_python.txt') as file_object:
    lines = file_object.readlines()

for line in lines:
    print(line.strip())
