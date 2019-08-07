from setuptools import find_packages, setup, Command
import os
import pathlib
import shutil
import sys


AUTHOR = "Sri Kadimisetty"
AUTHOR_EMAIL = "s@sri.io"
PROGRAM_NAME = "action-hero"
PROGRAM_VERSION = "0.6.3"
DESCRIPTION = "Argparse Actions that pack a punch!"
URL = "https://github.com/kadimisetty/action-hero"
LICENSE = "MIT"
PYTHON_REQUIREMENTS = ">=3.5.0"
README_FILENAME = "README.md"
REQUIRED_INSTALLS = ["requests"]
CLASSIFIERS = (
    [
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Topic :: Terminals",
        "Natural Language :: English",
    ],
)


# INSTRUCTIONS
# ------------
# 1. Update setup.py values above the fold
# 2. Use command `$ python setup.py publish` to clean/build/check/publish


# -------------- STAY ABOVE THIS FOLD ------------------->o--------------------


# CONTENTS BELOW THE FOLD
# -----------------------
# 1. Helpers to extract long description from README
# 2. Custom setuptools.Command `publish` to clean/build/check/publish
# 3. setup.py filled in with values specified above the fold


def get_long_description(filename=README_FILENAME):
    """Return contents of long description from contents of filename"""
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def get_long_description_content_type(filename=README_FILENAME):
    """Return content-type of long description from content-type of filename"""
    suffix = pathlib.Path(filename).suffix
    content_types = {"md": "text/markdown", "rst": "text/x-rst"}
    return content_types.get(suffix, "text/plain")


class PublishCommand(Command):
    """Add command `publish` to upload to PyPi

    Credits:
        - https://setuptools.readthedocs.io/en/latest/setuptools.html? \
            highlight=Command#adding-commands
        - Inspired by @kennethreitz/setup.py


    """

    description = "Clean/build/check/publish project to PyPi"
    user_options = []

    @staticmethod
    def display(update, state="normal"):
        """Print given update"""
        state_symbols = {
            "normal": "·",
            "ended": "\N{check mark}",
            "error": "!",
        }
        print("setup.py {} {}".format(state_symbols[state], update))

    def run(self):
        """Runs the Command"""
        for stage in ["clean", "build", "check", "publish"]:
            # Run stage with confirmation
            prompt = (
                "\x1b[5;30;42m "
                + "{}? ".format(stage).rjust(9)
                + "\x1b[0m [Yn]: "
            )
            if input(prompt) in "yY":
                getattr(self, stage)()
            else:
                self.display("skipping {}".format(stage))
        sys.exit()

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def publish(self):
        """Publish to PyPi"""
        self.display("publishing to PyPi with twine")
        if os.system("twine upload dist/*") == 0:
            self.display("published to PyPi with twine", state="ended")
        else:
            self.display("failed publishing to PyPi with twine", state="error")
            sys.exit()

    def check(self):
        """Check with twine"""
        self.display("checking with twine")
        if os.system("twine check dist/*") == 0:
            self.display("checked with twine", state="ended")
        else:
            self.display("failed checking with twine. Please fix. Exiting…", state="error")
            sys.exit()

    def build(self):
        """Build"""
        try:
            self.display("building source and wheel distribution")
            os.system("{0} setup.py sdist bdist_wheel".format(sys.executable))
            self.display("built source and wheel distribution", state="ended")

        except OSError:
            self.display(
                "failed removing previous builds. Plese fix. Exiting…", state="error"
            )
            sys.exit()

    def clean(self):
        """Remove previous builds"""
        try:
            self.display("removing previous builds", state="normal")
            shutil.rmtree("dist")
            self.display("removed previous builds", state="ended")

        except FileNotFoundError:
            self.display("no previous builds found.", state="error")

        except OSError:
            self.display(
                "failed removing previous builds. Please fix. Exiting…", state="error"
            )
            sys.exit()


setup(
    name=PROGRAM_NAME,
    version=PROGRAM_VERSION,
    description=DESCRIPTION,
    long_description=get_long_description(),
    long_description_content_type=get_long_description_content_type(),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    python_requires=PYTHON_REQUIREMENTS,
    url=URL,
    license=LICENSE,
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=REQUIRED_INSTALLS,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Topic :: Terminals",
        "Natural Language :: English",
    ],
    cmdclass={"publish": PublishCommand},
)
