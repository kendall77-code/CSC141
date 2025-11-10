# Exercise 10-3: Simpler Code

# Read the entire file and print its contents
print("📘 Reading the entire file:\n")

with open('learning_python.txt') as file_object:
    contents = file_object.read()
    print(contents)

# Read and print each line directly from splitlines(), no temporary variable
print("\n📘 Reading file line by line using splitlines():\n")

with open('learning_python.txt') as file_object:
    for line in file_object.read().splitlines():
        print(line)