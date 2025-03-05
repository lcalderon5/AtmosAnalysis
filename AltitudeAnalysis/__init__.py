import matplotlib.pyplot as plt
from cycler import cycler

# Set plotting preferences
cycl = (cycler(color=['#0C5DA5', '#00B945', '#FF9500', '#FF2C00', '#845B97', '#474747', '#9e9e9e'])
         + cycler(linestyle=['-', '--', '-.', ':', '-', '--', '-.'])) # You need to have as many colors as linestyles

plt.rcParams.update({

    # General
    'font.size': 16,
    'figure.figsize': (12, 7),

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
    'axes.prop_cycle' : cycl,
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