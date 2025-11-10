# Exercise 10-8: Cats and Dogs

filenames = ['cats.txt', 'dogs.txt']

for filename in filenames:
    try:
        print(f"\n📖 Reading {filename}:")
        with open(filename) as file_object:
            contents = file_object.read()
    except FileNotFoundError:
        print(f"❌ Sorry, the file '{filename}' was not found.")
    else:
        print(contents.strip())
