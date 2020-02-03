AUTHOR = "Sri Kadimisetty"
AUTHOR_EMAIL = "s@sri.io"
NAME = "action-hero"
VERSION = "0.7.0"
DESCRIPTION = "Make powerful CLIs with argparse actions that pack a punch! "
URL = "https://github.com/kadimisetty/action-hero"
LICENSE = "MIT"
PYTHON_REQUIRES = ">=3.5.0"
README_FILENAME = "README.md"
INSTALL_REQUIRES = ["requests", "pyyaml"]
CLASSIFIERS = [
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
]


# INSTRUCTIONS
# ------------
# 1. Setup setup.py values in uppercase above the fold
# 2. Use command `$ python setup.py make` to clean/build/check/publish


# ---------------- STAY ABOVE THE FOLD ------------------>o--------------------
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ Stay above the fold. For under, swim dangerous sharks ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ above-the-fold v0.0.1 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ What are you doing down here? ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ Didn't I just warn you about dangerous sharks?  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ Have you even seen Jaws! or Jaws 2!! or Jaws 3D!!! or Jaws Revenge!!!!  ~
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ If you insist on going anyway — you're gonna need a bigger boat ~ ~ ~ ~ ~
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


# CONTENTS BELOW THE FOLD
# -----------------------
# 1. Helpers to extract long description from README.
# 2. Custom setuptools.Command `make` to clean/build/check/publish.
# 3. setup.py filled in with values specified above the fold.


import os  # noqa: E402 # pylint: disable=C0413
import pathlib  # noqa: E402 # pylint: disable=C0413
import shutil  # noqa: E402 # pylint: disable=C0413
import sys  # noqa: E402 # pylint: disable=C0413
from setuptools import find_packages  # noqa: E402 # pylint: disable=C0413
from setuptools import setup  # noqa: E402 # pylint: disable=C0413
from setuptools import Command  # noqa: E402 # pylint: disable=C0413


def get_long_description(readme_filename=README_FILENAME):
    """Return contents of long description from contents of filename"""
    with open(readme_filename, "r", encoding="utf-8") as readme:
        return readme.read()


def get_long_description_content_type(filename=README_FILENAME):
    """Return content-type of long description from content-type of filename"""
    suffix = pathlib.Path(filename).suffix
    content_types = {"md": "text/markdown", "rst": "text/x-rst"}
    return content_types.get(suffix, "text/plain")


class MakeCommand(Command):
    """Add command `make` to upload to PyPi

    setuptools runs the function `run` which will in turn, with confirmation,
    do clean, build, check and publish.

    Credits:
        - http://code.nabla.net/doc/setuptools/api/setuptools/ \
            setuptools.Command.html
        - https://setuptools.readthedocs.io/en/latest/setuptools.html? \
            highlight=Command#adding-commands
        - Inspired by @kennethreitz/setup.py

    """

    description = "clean/build/check/publish project to PyPi"
    user_options = []

    def initialize_options(self):
        """Set default values for all the options supported by command"""

    def finalize_options(self):
        """Set final values for all the options supported by command"""

    @staticmethod
    def display(update, state="normal"):
        """Print given update"""
        state_symbols = {
            "normal": "·",
            "ended": "\N{check mark}",
            "error": "!",
        }
        if state == "error":
            print(
                "setup.py "
                + "\x1b[1;31;40m"
                + "{}".format(state_symbols[state])
                + "\x1b[0m [Yn]:"
                + " {}".format(update)
            )
        else:
            print("setup.py {} {}".format(state_symbols[state], update))

    def run(self):
        """Runs the Command"""
        for stage in ["clean", "build", "check", "publish"]:
            # Run stage with confirmation
            prompt = (
                # "\x1b[5;30;42m "
                "\x1b[1;37;44m "
                + "{}? ".format(stage).rjust(9)
                + "\x1b[0m [Yn]: "
            )
            if input(prompt) in "yY":
                getattr(self, stage)()
            else:
                self.display("skipping {}".format(stage))
        sys.exit()

    def publish(self):
        """Publish to PyPi"""
        task = "publishing to PyPi with twine"
        self.display(task)
        if os.system("twine upload dist/*") == 0:
            self.display("finished " + task, state="ended")
        else:
            self.display(
                "failed " + task + ". Please fix. Exiting…", state="error"
            )
            sys.exit()

    def check(self):
        """Check with twine"""
        task = "checking with twine"
        self.display(task)
        if os.system("twine check dist/*") == 0:
            self.display("finished " + task, state="ended")
        else:
            self.display(
                "failed " + task + ". Please fix. Exiting…", state="error"
            )
            sys.exit()

    def build(self):
        """Build"""
        task = "building source and wheel distribution"
        try:
            self.display(task, state="normal")
            os.system("{0} setup.py sdist bdist_wheel".format(sys.executable))
            self.display("finished " + task, state="ended")

        except OSError:
            self.display(
                "failed " + task + ". Please fix. Exiting…", state="error"
            )
            sys.exit()

    def clean(self):
        """Remove previous builds"""
        task = "removing previous builds"
        try:
            self.display(task, state="normal")
            shutil.rmtree("dist")
            self.display("finished " + task, state="ended")

        except FileNotFoundError:
            self.display("no previous builds found.", state="error")

        except OSError:
            self.display(
                "failed " + task + ". Please fix. Exiting…", state="error"
            )
            sys.exit()


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=get_long_description(),
    long_description_content_type=get_long_description_content_type(),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    python_requires=PYTHON_REQUIRES,
    url=URL,
    license=LICENSE,
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    classifiers=CLASSIFIERS,
    cmdclass={"make": MakeCommand},
)
