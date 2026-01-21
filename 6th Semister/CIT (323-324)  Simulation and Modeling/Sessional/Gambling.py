import random
import matplotlib.pyplot as plt

def monte_carlo_pi(num_points=1000):
    inside_x, inside_y = [], []
    outside_x, outside_y = [], []
    inside = 0

    # Simulation loop
    for _ in range(num_points):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        if x**2 + y**2 <= 1:
            inside += 1
            inside_x.append(x)
            inside_y.append(y)
        else:
            outside_x.append(x)
            outside_y.append(y)

    # Estimate π
    pi_estimate = 4 * inside / num_points

    # Visualization
    fig, ax = plt.subplots(figsize=(6,6))
    ax.scatter(inside_x, inside_y, color="green", s=10, label="Inside Circle")
    ax.scatter(outside_x, outside_y, color="red", s=10, label="Outside Circle")

    # Draw quarter circle boundary
    circle = plt.Circle((0,0), 1, color="blue", fill=False, linewidth=2, label="Quarter Circle")
    ax.add_artist(circle)

    # Formatting
    ax.set_aspect('equal')
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    plt.title(f"Monte Carlo Simulation (Estimated π = {pi_estimate:.4f})")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.legend()
    plt.show()

    return pi_estimate

# Run simulation
pi_value = monte_carlo_pi(10000000)
print("Estimated π:", pi_value)