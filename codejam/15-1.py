import matplotlib.pyplot as plt # type: ignore

# Generate the first five cubic numbers
x_values_small = list(range(1, 6))
y_values_small = [x**3 for x in x_values_small]

# Plot the first five cubic numbers
plt.figure(figsize=(6, 4))
plt.scatter(x_values_small, y_values_small, s=40)
plt.title("First Five Cubic Numbers")
plt.xlabel("Value")
plt.ylabel("Cube of Value")
plt.grid(True)
plt.show()

# Generate the first 5,000 cubic numbers
x_values_large = list(range(1, 5001))
y_values_large = [x**3 for x in x_values_large]

# Plot the first 5,000 cubic numbers
plt.figure(figsize=(8, 6))
plt.scatter(x_values_large, y_values_large, s=1)
plt.title("First 5,000 Cubic Numbers")
plt.xlabel("Value")
plt.ylabel("Cube of Value")
plt.grid(True)
plt.show()
