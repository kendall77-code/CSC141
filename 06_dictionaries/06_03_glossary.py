# 6-3. Glossary
# Create a dictionary to store programming words and their meanings
glossary = {
    'variable': 'A name used to store a value that can change during the program.',
    'loop': 'A structure for repeating a block of code multiple times.',
    'function': 'A block of reusable code that performs a specific task.',
    'list': 'A collection of items in a particular order, enclosed in square brackets.',
    'dictionary': 'A collection of key-value pairs, enclosed in curly braces.'
}

# Print each word and its meaning neatly formatted
for word, meaning in glossary.items():
    print(f"{word.title()}:\n  {meaning}\n")