# Exercise 10-9: Silent Cats and Dogs

filenames = ['cats.txt', 'dogs.txt']

for filename in filenames:
    try:
        with open(filename) as file_object:
            contents = file_object.read()
    except FileNotFoundError:
        # Fail silently — do nothing if the file doesn’t exist
        pass
    else:
        print(f"\n📖 Reading {filename}:")
        print(contents.strip())
