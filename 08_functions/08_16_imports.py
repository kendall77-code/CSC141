# greetings.py

def greet_user(name):
    """Display a simple greeting."""
    print(f"Hello, {name.title()}! Welcome back.")

# imports_demo.py

# 1️⃣ Import the entire module
import greetings # type: ignore
greetings.greet_user("kendall")

# 2️⃣ Import a specific function
from greetings import greet_user # type: ignore
greet_user("Kam")

# 3️⃣ Import with an alias for the function
from greetings import greet_user as gu # type: ignore
gu("Brandon")

# 4️⃣ Import the module with an alias
import greetings as gr # type: ignore
gr.greet_user("Dave")

# 5️⃣ Import all functions from the module
from greetings import * # type: ignore
greet_user("Jermaine")