# Exercise 10-10: Common Words

# You can analyze any text files from Project Gutenberg — just place them in the same folder.
# Example: 'frankenstein.txt', 'pride_and_prejudice.txt', etc.

filenames = ['frankenstein.txt', 'pride_and_prejudice.txt']

for filename in filenames:
    try:
        with open(filename, encoding='utf-8') as file_object:
            contents = file_object.read()
    except FileNotFoundError:
        print(f"❌ Sorry, the file '{filename}' was not found.")
    else:
        # Convert to lowercase for consistent counting
        lower_text = contents.lower()

        # Count occurrences of 'the' (approximate count)
        count_the = lower_text.count('the')
        # Count occurrences of 'the ' (more accurate count)
        count_the_space = lower_text.count('the ')

        print(f"\n📖 Results for {filename}:")
        print(f"Occurrences of 'the': {count_the:,}")
        print(f"Occurrences of 'the ' (with space): {count_the_space:,}")
