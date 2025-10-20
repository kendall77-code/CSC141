# 8-14. Cars

def make_car(manufacturer, model, **car_info):
    """Store information about a car in a dictionary."""
    car_info['manufacturer'] = manufacturer.title()
    car_info['model'] = model.title()
    return car_info

# Call the function with required and additional keyword arguments
car = make_car('Toyota', 'Camry', color='Dark Grey', tow_package=True)

# Print the resulting dictionary
print(car)