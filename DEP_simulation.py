# Property of Oregon Health and Science Unviersity
# Created By Jason Ware (warej@ohsu.edu) 2023

# This program provides a visualization of trapping dielectrophoresis and is not intended for mathematical simulations of DEP particle isolation

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
from matplotlib.lines import Line2D

# Constants
NUM_SMALL_PARTICLES = 200
RADIUS_SMALL_PARTICLE = 3
NUM_LARGE_PARTICLES = 200
RADIUS_LARGE_PARTICLE = 20
RADIUS_ELECTRODE = 5

DIFFUSION_DISTANCE = 0.001

def calculate_edge_distances(x, y):
    # Coordinates of the gray circles
    electrode1_center = (20, 20)
    electrode2_center = (-20, 20)
    electrode3_center = (-20, -20)
    electrode4_center = (20, -20)

    # Calculate distance to electrode centers
    dist_to_electrode1 = np.sqrt((x - electrode1_center[0])**2 + (y - electrode1_center[1])**2)
    dist_to_electrode2 = np.sqrt((x - electrode2_center[0])**2 + (y - electrode2_center[1])**2)
    dist_to_electrode3 = np.sqrt((x - electrode3_center[0])**2 + (y - electrode3_center[1])**2)
    dist_to_electrode4 = np.sqrt((x - electrode4_center[0])**2 + (y - electrode4_center[1])**2)

    dist_array = np.array([dist_to_electrode1, dist_to_electrode2, dist_to_electrode3, dist_to_electrode4])

    if np.min(dist_array) == dist_to_electrode1:
        dist_to_electrode = dist_to_electrode1
        electrode_center = electrode1_center
    elif np.min(dist_array) == dist_to_electrode2:
        dist_to_electrode = dist_to_electrode2
        electrode_center = electrode2_center
    elif np.min(dist_array) == dist_to_electrode3:
        dist_to_electrode = dist_to_electrode3
        electrode_center = electrode3_center
    else:
        dist_to_electrode = dist_to_electrode4
        electrode_center = electrode4_center

    if dist_to_electrode <= 5 and dist_to_electrode >= 4.8:
        return 0, 0

    if dist_to_electrode < 4.8:
        return 1*(x - electrode_center[0]), 1*(y - electrode_center[1])
    else:
        return -1*(x - electrode_center[0]), -1*(y - electrode_center[1])

# Initialize the figure and subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
plt.subplots_adjust(bottom=0.2)

# Slider parameters
volt_slider_ax = plt.axes([0.15, 0.09, 0.7, 0.03])
volt_slider = Slider(volt_slider_ax, 'Voltage', 0.0, 20, valinit=0)
freq_slider_ax = plt.axes([0.15, 0.06, 0.7, 0.03])
freq_slider = Slider(freq_slider_ax, 'Frequency', 0.0, 30000, valinit=14000)
temp_slider_ax = plt.axes([0.15, 0.03, 0.7, 0.03])
temp_slider = Slider(temp_slider_ax, 'Temperature', 0, 100, valinit=25)
flow_slider_ax = plt.axes([0.15, 0.00, 0.7, 0.03])
flow_slider = Slider(flow_slider_ax, 'Flow ->', 0, 15, valinit=0)

# Create small spheres
np.random.seed()
x_small = np.random.uniform(-40, 40, NUM_SMALL_PARTICLES)
y_small = np.random.uniform(-40, 40, NUM_SMALL_PARTICLES)
scatter_small = ax1.scatter(x_small, y_small, s=RADIUS_SMALL_PARTICLE ** 2, c='blue', alpha=0.6)

np.random.seed()
x_large = np.random.uniform(-40, 40, NUM_LARGE_PARTICLES)
y_large = np.random.uniform(-40, 40, NUM_LARGE_PARTICLES)
scatter_large = ax1.scatter(x_large, y_large, s=RADIUS_LARGE_PARTICLE ** 2, c='red', alpha=0.6)

# Create electrodes
circle1 = plt.Circle((20, 20), RADIUS_ELECTRODE, fc='grey', alpha=0.5)
circle2 = plt.Circle((-20, 20), RADIUS_ELECTRODE, fc='gray', alpha=0.5)
circle3 = plt.Circle((-20, -20), RADIUS_ELECTRODE, fc='grey', alpha=0.5)
circle4 = plt.Circle((20, -20), RADIUS_ELECTRODE, fc='gray', alpha=0.5)

ax1.set_xlim(-40, 40)
ax1.set_ylim(-40, 40)
ax1.add_patch(circle1)
ax1.add_patch(circle2)
ax1.add_patch(circle3)
ax1.add_patch(circle4)
ax1.set_axis_off()
ax1.set_aspect('equal', 'box')

# Data for the frequency vs DEP Force plot
frequency = np.array([0,9999,10000,24999,25000,30000])
small_particles = np.array([0,0,1,1,1,1])
large_particles = np.array([0,0,1,1,-0.5,-0.5])

# Plot the frequency vs DEP Force
ax2.plot(frequency, large_particles, color='red', linewidth = 7, label='large particles')
ax2.plot(frequency, small_particles, color='blue', linewidth = 4, label='small particles')


ax2.set_xlim(0, 30000)
ax2.set_ylim(-1, 2)
ax2.set_xlabel('Frequency')
ax2.set_ylabel('DEP Force')
ax2.legend()

# Add the vertical line
vertical_line = Line2D([freq_slider.val, freq_slider.val], [-1, 2], color='black', linestyle='--', linewidth=1)
ax2.add_line(vertical_line)

# Function to update the animation
def update(frame):
    diffusion_strength = 0.1*temp_slider.val**2
    voltage = volt_slider.val/3
    # Update positions of small spheres
    distt = 5
    for i in range(NUM_SMALL_PARTICLES):
        distx, disty = calculate_edge_distances(x_small[i], y_small[i])
        if freq_slider.val >= 10000 and distx != 0 and disty != 0:
            distt = np.sqrt(distx**2 + disty**2)
            x_small[i] += 5*((distx) * voltage)/(distt**3)
            y_small[i] += 5*((disty) * voltage)/(distt**3)

        x_small[i] += (np.random.uniform(-1, 1) * DIFFUSION_DISTANCE * diffusion_strength)
        y_small[i] += (np.random.uniform(-1, 1) * DIFFUSION_DISTANCE * diffusion_strength)

        if distt >= 6 or volt_slider.val <= 3:
            x_small[i] += flow_slider.val/20

    scatter_small.set_offsets(np.column_stack((x_small, y_small)))

    for i in range(NUM_LARGE_PARTICLES):
        distx, disty = calculate_edge_distances(x_large[i], y_large[i])
        if freq_slider.val >= 10000 and distx != 0 and disty != 0:
            distt = np.sqrt(distx**2 + disty**2)
            pn = -1
            if freq_slider.val > 25000:
                pn = 1
            if distt < 5:
                pn = -1
            if distt > 22 and pn == 1:
                pn = 0
            x_large[i] -= pn*5*((distx) * voltage)/(distt**3)
            y_large[i] -= pn*5*((disty) * voltage)/(distt**3)
        x_large[i] += (np.random.uniform(-1, 1) * DIFFUSION_DISTANCE * diffusion_strength) + flow_slider.val/20
        y_large[i] += (np.random.uniform(-1, 1) * DIFFUSION_DISTANCE * diffusion_strength)
    

    scatter_large.set_offsets(np.column_stack((x_large, y_large)))

    vertical_line.set_xdata([freq_slider.val, freq_slider.val])

# Animation function
anim = FuncAnimation(fig, update, frames=500, interval=100, blit=False)

# Display the plot
plt.show()
