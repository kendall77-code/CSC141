"""
Exercise 8-17 — Styling Functions

This script presents three functions from Chapter 8 rewritten to follow clean,
consistent styling: snake_case names, clear docstrings, sensible defaults,
consistent spacing, and concise, readable example calls.
"""


def favorite_book(title: str) -> None:
    """Print a short message about a favorite book.

    Args:
        title: The title of the book.
    """
    print(f"One of my favorite books is {title.title()}.")


def make_shirt(size: str = "large", message: str = "I love Python") -> None:
    """Summarize the shirt that is being made.

    Args:
        size: The shirt size (e.g., 'small', 'medium', 'large').
        message: The message to be printed on the shirt.
    """
    print(f"Making a {size} shirt with the message: '{message}'.")


def make_car(manufacturer: str, model: str, **options) -> dict:
    """Build a dictionary representing a car.

    Args:
        manufacturer: The car manufacturer.
        model: The model name.
        **options: Arbitrary keyword options (e.g., color='blue').

    Returns:
        A dictionary with car information combined with any extra options.
    """
    car = {
        "manufacturer": manufacturer.title(),
        "model": model.title(),
    }
    car.update(options)
    return car


def main() -> None:
    """Run simple demos for the styled functions."""
    # 1) favorite_book
    favorite_book("the last white man")

    # 2) make_shirt with defaults and overrides
    make_shirt()
    make_shirt(size="medium")
    make_shirt(size="small", message="Keep Coding!")

    # 3) make_car with extra options
    car = make_car("subaru", "outback", color="blue", tow_package=True)
    print(car)


if __name__ == "__main__":
    main()