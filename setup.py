from setuptools import find_packages, setup

setup(
    name="Action Heroes",
    version="0.1.0",
    description="Argparse actions for one and all!",
    author="Sri Kadimisetty",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=[],
)
