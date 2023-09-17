from setuptools import setup, find_packages

setup(
    name="gooeycade",
    version="0.1.0",
    description="",  # Add a description if you have one
    author="Grayson Miller",
    author_email="grayson.miller124@gmail.com",
    url="",  # Add a URL if you have one
    packages=find_packages(),
    install_requires=["python>=3.10", "arcade>=2.6.17", "numpy>=1.24.2"],
    entry_points={
        "console_scripts": [
            "gcade=gooeycade.__main__:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
