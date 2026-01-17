import random

# Initialize position
x = 0
y = 0

# List to store step details (optional, for table output)
steps = []

# Simulate 50 steps
for step in range(1, 51):
    rand = random.randint(0, 9)
    if rand <= 4:  # 0-4: F (50%)
        direction = 'F'
        y += 1
    elif rand <= 7:  # 5-7: L (30%)
        direction = 'L'
        x -= 1
    else:  # 8-9: R (20%)
        direction = 'R'
        x += 1
    steps.append((step, rand, direction, x, y))

# Print the simulation table
print("Step | Random Number | Direction | x | y")
print("-" * 40)
for s in steps:
    print(f"{s[0]:4} | {s[1]:13} | {s[2]:9} | {s[3]:2} | {s[4]:2}")

# Final position
print(f"\nFinal position after 50 steps: ({x}, {y})")