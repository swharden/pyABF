
"""
Demonstrate how to place text in arbitrary locations on a matplotlib figure.
"""

import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    fig = plt.figure(figsize=(6, 4))
    plt.title("some title")
    plt.ylabel("vertical axis")
    plt.xlabel("horizontal axis")
    plt.grid(alpha=.5, ls='--')
    plt.plot(np.random.random_sample(100), '.', ms=20, alpha=.5)
    plt.tight_layout()
    fig.text(0.02, 0.97, "upper text goes here", transform=plt.gca().transAxes,
             fontsize=10, verticalalignment='top', family='monospace', 
             color='r', alpha=.7)
    fig.text(0.02, 0.03, "lower text goes here", transform=plt.gca().transAxes,
             fontsize=10, verticalalignment='bottom', family='monospace', 
             color='r', alpha=.7)
    plt.show()
    print("DONE")
