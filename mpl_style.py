import matplotlib.pyplot as plt
from cycler import cycler

# Set plotting preferences
# These cyclers are basically color and line themes for the plots
cycl_std = (cycler(color=['#0C5DA5', '#00B945', '#FF9500', '#FF2C00', '#845B97', '#474747', '#9e9e9e'])
         + cycler(linestyle=['-', '--', '-.', ':', '-', '--', '-.'])) # You need to have as many colors as linestyles

cycl_ibm = (cycler(color=['#648FFF', '#785EF0', '#DC267F', '#FE6100', '#FFB000'])
         + cycler(linestyle=['-', '--', '-.', ':', '-'])) # You need to have as many colors as linestyles

cycl_deep = (cycler(color=['#1f3b73', '#1f6b3b', '#8b1e3f', '#d35400', '#5e2a84', '#704214', '#b8860b', '#116466', '#a83279', '#4b4e57', '#5d3a9b', '#008b8b', '#4b830d', '#d3545d', '#3c3f8f', '#c44536', '#0e6655', '#a67c00'])
         + cycler(linestyle=['-', '--', '-.', ':', '-', '--', '-.', ':', '-', '--', '-.', ':', '-', '--', '-.', ':', '-', '--'])) # You need to have as many colors as linestyles

cycl_pastel = (cycler(color=['#6c8ebf', '#8fbf6c', '#bf6c6c', '#e5a46c', '#b07fb0', '#c4a484', '#f2d16d', '#76b7b2', '#f3a6b3', '#b0b7c6', '#c2a2da', '#91d8e4', '#b7de79', '#f7c59f', '#7c83bc', '#f4a988', '#a4d4ae', '#e4b363'])
         + cycler(linestyle=['-', '--', '-.', ':', '-', '--', '-.', ':', '-', '--', '-.', ':', '-', '--', '-.', ':', '-', '--'])) # You need to have as many colors as linestyles

# Update the plot preferences (you can change these to your liking)
plt.rcParams.update({

    # General
    'font.size': 16,
    'figure.figsize': (12, 7),
    'figure.dpi': 100,

    # Grid
    'axes.grid': True,
    'grid.color': 'gray',
    'grid.linestyle': '--',
    'grid.linewidth': 0.5,
    'grid.alpha': 0.7,

    # Fonts
    'font.family': 'serif',
    # 'font.serif': ['Times New Roman'],

    # Colors and line styles
    'axes.prop_cycle' : cycl_ibm,
    'lines.linewidth': 2,

    # Legend
    'legend.frameon': False,

    # Set x axis
    'xtick.major.size' : 3,
    'xtick.major.width' : 0.5,
    'xtick.minor.size' : 1.5,
    'xtick.minor.width' : 0.5,
    'xtick.minor.visible' : True,
    'xtick.top' : True,

    # Set y axis
    'ytick.major.size' : 3,
    'ytick.major.width' : 0.5,
    'ytick.minor.size' : 1.5,
    'ytick.minor.width' : 0.5,
    'ytick.minor.visible' : True,
    'ytick.right' : True,

    # Handle latex text
    'text.usetex': False,  # Ensures no external LaTeX installation is used
    'mathtext.fontset': 'dejavuserif',  # Ensures math text matches the rest of the text
    'font.family': 'serif',  # Match the font with your main font
    # 'font.serif': ['Times New Roman'],  # Change if needed

})
