import logging
import os
import shutil
import subprocess

from packaging import version
import pyinstaller_versionfile
from setuptools import Command, find_packages, setup

SCRIPT_DESCRIPTION = "Simulate mouse and keyboard activity on your computer"
SCRIPT_NAME = "MouseBot"
SCRIPT_VERSION = 1.1
INPUT_FILE = "./mouse_bot.py"
OUTPUT_FILE = "mouse_bot.exe"
VERSION_FILE = "version_info.txt"


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


class BuildCommand(Command):
    """Build script binary."""

    description = "Build script to .exe file"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self) -> bool:
        self.announce("Generating version file", level=logging.WARNING)
        v = version.parse(str(SCRIPT_VERSION))
        pyinstaller_versionfile.create_versionfile(
            output_file=VERSION_FILE,
            version=f"{str(v)}.0.0",
            company_name="FloZone",
            file_description=SCRIPT_DESCRIPTION,
            internal_name=SCRIPT_NAME,
            legal_copyright="Copyright © 2024",
            original_filename=OUTPUT_FILE,
            product_name=SCRIPT_NAME,
        )
        self.announce("Building binary", level=logging.WARNING)
        res = subprocess.run(
            [
                "pyinstaller",
                "--clean",
                "--onefile",
                "--icon=color.ico",
                "--add-data=color.ico:.",
                "--add-data=grey.ico:.",
                f"--version-file={VERSION_FILE}",
                f"./{INPUT_FILE}",
            ]
        )
        if res.returncode == 0:
            self.announce(f"\nBinary file generated to './dist/{OUTPUT_FILE}'", level=logging.WARNING)
            return True
        else:
            return False


class CleanCommand(Command):
    """Clean temporary files."""

    description = "Clean temporary files"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self) -> bool:
        self.announce("Cleaning project...", level=logging.WARNING)
        paths = ["build", "dist", "__pycache__", "mouse_bot.spec", VERSION_FILE]
        for p in paths:
            if os.path.isdir(p):
                self.announce(f"Cleaning ./{p}/", level=logging.WARNING)
                shutil.rmtree(p)
            elif os.path.isfile(p):
                self.announce(f"Cleaning ./{p}", level=logging.WARNING)
                os.remove(p)
        return True


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
        return (
            subprocess.run(
                [
                    "black",
                    "--target-version",
                    "py38",
                    "-l",
                    "120",
                    INPUT_FILE,
                ],
            ).returncode
            == 0
        )


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


setup(
    name=SCRIPT_NAME,
    version=SCRIPT_VERSION,
    author="FloZone",
    description=SCRIPT_DESCRIPTION,
    long_description=read("README.md"),
    packages=find_packages(),
    cmdclass={
        "clean": CleanCommand,
        "build": BuildCommand,
        "fmt": FormatCommand,
        "lint": LintCommand,
    },
)
