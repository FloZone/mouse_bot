import distutils.cmd
import logging
import os
import subprocess

from setuptools import find_packages, setup, Command

INPUT_FILE = "./mouse_bot.py"


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


class LintCommand(Command):
    """Lint with flake8."""

    description = "run flake8 on source files"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self) -> bool:
        self.announce("Linting...", level=logging.WARNING)

        self.announce("flake8 pass...", level=logging.WARNING)
        return subprocess.run(["flake8", INPUT_FILE]).returncode == 0


class FormatCommand(Command):
    """Format with black."""

    description = "Run isort and black on source files"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self) -> bool:
        self.announce("Formatting...", level=logging.WARNING)

        self.announce("isort pass...", level=logging.WARNING)
        if subprocess.run(["isort", "-rc", "--atomic", INPUT_FILE]).returncode != 0:
            return False

        self.announce("black pass...", level=logging.WARNING)
        return subprocess.run(
            [
                "black",
                "--target-version",
                "py38",
                "-l",
                "120",
                INPUT_FILE,
            ],
        ).returncode == 0


setup(
    name="MouseBot",
    version=1.0,
    author="FloZone",
    description="Simulate mouse and keyboard activity on your computer",
    long_description=read("README.md"),
    packages=find_packages(),
    cmdclass={
        "lint": LintCommand,
        "fmt": FormatCommand,
    },
)
