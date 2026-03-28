import pygame
import pygwidgets # type: ignore


WINDOW_WIDTH = 700
WINDOW_HEIGHT = 380
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (20, 40, 90)
RED = (170, 30, 30)


pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("GUI Temperature Converter")
clock = pygame.time.Clock()


# Support both possible class names used in different pygwidgets versions.
InputClass = pygwidgets.TextInput if hasattr(pygwidgets, "TextInput") else pygwidgets.InputText


def build_text_input():
    """Create the temperature input widget with compatibility fallbacks."""
    try:
        return InputClass(window, (40, 90), width=180)
    except TypeError:
        try:
            return InputClass(window, (40, 90), "", width=180)
        except TypeError:
            return InputClass(window, (40, 90), "")


def get_widget_value(widget):
    if hasattr(widget, "getValue"):
        return widget.getValue()
    if hasattr(widget, "getText"):
        return widget.getText()
    return ""


def set_widget_value(widget, text):
    if hasattr(widget, "setValue"):
        widget.setValue(text)
        return
    if hasattr(widget, "setText"):
        widget.setText(text)


def make_radio_button(location, text, group, selected=False):
    """Build radio buttons with a few constructor patterns for compatibility."""
    try:
        return pygwidgets.TextRadioButton(window, location, text, group=group, value=selected)
    except TypeError:
        try:
            return pygwidgets.TextRadioButton(window, location, text, group, selected)
        except TypeError:
            return pygwidgets.TextRadioButton(window, location, text, group)


def convert_temperature():
    raw_text = str(get_widget_value(input_temp)).strip()

    if raw_text == "":
        set_widget_value(output_text, "Enter a number first.")
        return

    try:
        temp_value = float(raw_text)
    except ValueError:
        set_widget_value(output_text, "Invalid number. Try again.")
        return

    if get_widget_value(c_to_f_radio):
        # F = C * 9/5 + 32
        answer = temp_value * 9 / 5 + 32
        set_widget_value(output_text, f"{temp_value:.2f} C = {answer:.2f} F")
    else:
        # C = (F - 32) / (9/5)
        answer = (temp_value - 32) / (9 / 5)
        set_widget_value(output_text, f"{temp_value:.2f} F = {answer:.2f} C")


# Widgets required by rubric
prompt_text = pygwidgets.DisplayText(window, (40, 30), "Enter temperature:", textColor=DARK_BLUE, fontSize=34)
input_temp = build_text_input()

c_to_f_radio = make_radio_button((40, 150), "Celsius to Fahrenheit", group=1, selected=True)
f_to_c_radio = make_radio_button((40, 190), "Fahrenheit to Celsius", group=1, selected=False)

convert_button = pygwidgets.TextButton(window, (40, 245), "Convert")
output_text = pygwidgets.DisplayText(window, (40, 305), "Result will show here.", textColor=RED, fontSize=30)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Rubric event A: pressing Enter in input box
        input_entered = input_temp.handleEvent(event)
        if input_entered:
            convert_temperature()

        # Rubric event B: changing selected radio button
        c_selected = c_to_f_radio.handleEvent(event)
        f_selected = f_to_c_radio.handleEvent(event)
        if c_selected or f_selected:
            convert_temperature()

        # Rubric event C: pressing button
        if convert_button.handleEvent(event):
            convert_temperature()

    window.fill(WHITE)

    prompt_text.draw()
    input_temp.draw()
    c_to_f_radio.draw()
    f_to_c_radio.draw()
    convert_button.draw()
    output_text.draw()

    pygame.display.update()
    clock.tick(60)


pygame.quit()
