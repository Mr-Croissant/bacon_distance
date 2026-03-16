from setuptools import find_packages, setup

setup(
    name="Bacon-Backend",
    version="1.0",
    description="bacon distance",
    author="Ely",
    packages=find_packages(),
    install_requires=["flask", "pandas"],
)
