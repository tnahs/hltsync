#!/usr/bin/env python3

import os
import sys
import shutil
import pathlib
from typing import Union

from .errors import ApplicationError


class Utilities:
    def __init__(self, app):

        self.app = app

    def delete_dir(self, path: pathlib.PosixPath) -> None:

        try:
            shutil.rmtree(path)
        except OSError:
            pass
        except Exception as error:
            raise ApplicationError(repr(error), self.app)

    def make_dir(self, path: pathlib.PosixPath) -> None:

        try:
            os.makedirs(path)
        except FileExistsError:
            pass
        except OSError as error:
            raise ApplicationError(f"{error.filename} - {error.strerror}", self.app)
        except Exception as error:
            raise ApplicationError(repr(error), self.app)

    def copy_dir(self, src: pathlib.PosixPath, dest: pathlib.PosixPath) -> None:

        try:
            shutil.copytree(src, dest)
        except OSError as error:
            raise ApplicationError(f"{error.filename} - {error.strerror}")
        except Exception as error:
            raise ApplicationError(repr(error), self.app)

    def chunk_data(self, data: list, chunk_size=100):
        """ Instead of sending a long list of annotations all at once, this
        splits the list into a list of `chunk_size` lists. This helps prevent
        Gateway Timeout (504) error. """
        return [data[x : x + chunk_size] for x in range(0, len(data), chunk_size)]

    def to_lowercase(self, input_: Union[list, str, dict]) -> Union[list, str, dict]:

        if type(input_) is str:
            return input_.lower()

        elif type(input_) is list:
            return [v.lower() for v in input_]

        elif type(input_) is dict:
            return dict((k, v.lower()) for k, v in input_.items())

    def print_progress(self, current_iteration, total_iteration, max_bar=50):
        """ TODO: Clean how this is implemented inside of a loop.

        Call in a loop to create terminal progress bar. """

        completed_percent = f"{100 * (current_iteration / float(total_iteration)):.1f}"
        completed_bar = int(round(max_bar * current_iteration / float(total_iteration)))

        bar = f"{'▓' * completed_bar}{'░' * (max_bar - completed_bar)}"

        sys.stdout.write(f"\r{bar} {completed_percent}%"),

        if current_iteration == total_iteration:
            sys.stdout.write("\n")

        sys.stdout.flush()
