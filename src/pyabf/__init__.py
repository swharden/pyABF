"""
this is a PyPy placeholder for the pyABF project
"""

__version__ = '0.0.1'

def info():
    """display information."""
    print("this module is working!")
    print(__file__)

__all__ = ('info')

if __name__=="__main__":
    print("DO NOT RUN THIS SCRIPT DIRECTLY")
    info()