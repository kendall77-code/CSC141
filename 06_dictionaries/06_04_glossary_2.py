# 6-4. Glossary 2
# Create a dictionary to store programming words and their meanings
glossary = {
    'variable': 'A name used to store a value that can change during the program.',
    'loop': 'A structure for repeating a block of code multiple times.',
    'function': 'A block of reusable code that performs a specific task.',
    'list': 'A collection of items in a particular order, enclosed in square brackets.',
    'dictionary': 'A collection of key-value pairs, enclosed in curly braces.',
    'string': 'A sequence of characters enclosed in quotes.',
    'integer': 'A whole number, positive or negative, without decimals.',
    'boolean': 'A data type that can be either True or False.',
    'tuple': 'An ordered, immutable collection of items.',
    'conditional': 'A statement that runs code only if a certain condition is true.'
}

# Loop through the dictionary to print each word and its meaning
for word, meaning in glossary.items():
    print(f"{word.title()}:\n  {meaning}\n")