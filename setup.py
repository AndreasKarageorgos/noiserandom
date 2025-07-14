from setuptools import setup, find_packages

setup(
    name="NoiseRandom",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "gmpy2"
    ],
    license="MIT License"
)