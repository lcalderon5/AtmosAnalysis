import pymsis as msis
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt


pastel_colors = [
    "#6c8ebf",      # Soft Blue
    "#8fbf6c",     # Soft Green
    "#bf6c6c",       # Soft Red
    "#e5a46c",    # Soft Orange
    "#b07fb0",    # Soft Purple
    "#c4a484",     # Soft Brown
    "#f2d16d",    # Soft Yellow
    "#76b7b2",      # Soft Teal
    "#f3a6b3",      # Soft Pink
    "#b0b7c6",      # Soft Gray
    "#c2a2da",  # Soft Lavender
    "#91d8e4",      # Soft Cyan
    "#b7de79",      # Soft Lime
    "#f7c59f",     # Soft Peach
    "#7c83bc",    # Soft Indigo
    "#f4a988",    # Soft Salmon
    "#a4d4ae",      # Soft Mint
    "#e4b363",      # Soft Gold
]

deep_colors = [
    "#1f3b73",      # Deep Blue
    "#1f6b3b",     # Deep Green
    "#8b1e3f",       # Deep Red
    "#d35400",    # Deep Orange
    "#5e2a84",    # Deep Purple
    "#704214",     # Deep Brown
    "#b8860b",    # Deep Yellow
    "#116466",      # Deep Teal
    "#a83279",      # Deep Pink
    "#4b4e57",      # Deep Gray
    "#5d3a9b",  # Deep Lavender
    "#008b8b",      # Deep Cyan
    "#4b830d",      # Deep Lime
    "#d3545d",     # Deep Peach
    "#3c3f8f",    # Deep Indigo
    "#c44536",    # Deep Salmon
    "#0e6655",      # Deep Mint
    "#a67c00",      # Deep Gold
]

ibm_colors = [
    "#648FFF",  # Blue
    "#785EF0",  # Violet
    "#DC267F",  # Magenta
    "#FE6100",  # Orange
    "#FFB000"   # Yellow
]



x = np.linspace(0, 10, 100)
y = np.sin(x)

print(plt.style.available)

styles = ['Solarize_Light2', '_classic_test_patch', '_mpl-gallery', '_mpl-gallery-nogrid',
           'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale',
            'petroff10', 'seaborn-v0_8', 'seaborn-v0_8-bright', 'seaborn-v0_8-colorblind', 'seaborn-v0_8-dark',
            'seaborn-v0_8-dark-palette', 'seaborn-v0_8-darkgrid', 'seaborn-v0_8-deep', 'seaborn-v0_8-muted',
            'seaborn-v0_8-notebook', 'seaborn-v0_8-paper', 'seaborn-v0_8-pastel', 'seaborn-v0_8-poster',
            'seaborn-v0_8-talk', 'seaborn-v0_8-ticks', 'seaborn-v0_8-white', 'seaborn-v0_8-whitegrid',
            'tableau-colorblind10']

# for style in styles:
#     plt.style.use(style)
#     plt.plot(x, y)
#     plt.title(f"Style: {style}")
#     plt.show()

# Plot lines to compare the colors
fig, ax = plt.subplots(figsize=(8, 4))

# Plot the colors
for i, (color, hex) in enumerate(pastel_colors.items()):
    ax.plot([i, i], [0, 1], color=hex, label=color, linewidth=6)

# Set the labels
ax.set_xticks(range(len(pastel_colors)))
ax.set_xticklabels(list(pastel_colors.keys()), rotation=45, fontsize=12)
ax.set_yticks([])
ax.set_title('Pastel Colors', fontsize=16)


fig, ax1 = plt.subplots(figsize=(8, 4))

for i, (color, hex) in enumerate(deep_colors.items()):
    ax1.plot([i, i], [0, 1], color=hex, label=color, linewidth=6)

# Set the labels
ax1.set_xticks(range(len(deep_colors)))
ax1.set_xticklabels(list(deep_colors.keys()), rotation=45, fontsize=12)
ax1.set_yticks([])
ax1.set_title('Deep Colors', fontsize=16)

plt.show()


# Generate sample data
x = np.linspace(0, 10, 100)

# Create the figure
fig, ax = plt.subplots(figsize=(10, 6))

# Plot lines using IBM colors
for i, color in enumerate(ibm_colors):
    ax.plot(x, np.sin(x + i * 0.5), label=f"Line {i+1}", color=color, linewidth=2)

# Labels and legend
ax.set_xlabel("X-axis", fontsize=14)
ax.set_ylabel("Y-axis", fontsize=14)
ax.set_title("IBM Design Color Palette (Engineering-Friendly)", fontsize=16)
ax.legend(loc="upper right", fontsize=12)

# Grid for better readability
ax.grid(True, linestyle="--", alpha=0.6)

# Show the plot
plt.show()

# Test other color palettes
plt.style.use('seaborn-darkgrid')

# Create the figure
fig, ax = plt.subplots(figsize=(10, 6))

# Plot lines using the new colors
for i in range(5):
    ax.plot(x, np.sin(x + i * 0.5), label=f"Line {i+1}", linewidth=2)

# Labels and legend
ax.set_xlabel("X-axis", fontsize=14)
ax.set_ylabel("Y-axis", fontsize=14)
ax.set_title("Seaborn Dark Grid Color Palette", fontsize=16)
ax.legend(loc="upper right", fontsize=12)

plt.show()

