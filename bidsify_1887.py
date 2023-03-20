#! /usr/bin/env python3

"""
This script generates BIDS formatted directory for NDA Study 1887 downloaded from NDA.
"""

import argparse
import os
import platform
import shutil
from pathlib import Path


def existent(path):
    """
    Check if a path exists
    :param path: Path to check
    :return: Existent path as a string
    """
    path = Path(path)

    if not path.exists():
        raise argparse.ArgumentTypeError(f"{path} does not exist")

    return path


def readable(path):
    """
    Check if a path is readable
    :param path: Path to check
    :return: Readable path as a string
    """
    if not os.access(path, os.R_OK):
        raise argparse.ArgumentTypeError(f"{path} is not readable")
    return Path(path)


def writeable(path):
    """
    Check if a path is writeable
    :param path: Path to check
    :return: Writeable path as a string
    """
    if not os.access(path, os.W_OK):
        raise argparse.ArgumentTypeError(f"{path} is not writeable")
    return Path(path)


def executable(path):
    """
    Check if a path is executable
    :param path: Path to check
    :return: Executable path as a string
    """
    if not os.access(path, os.X_OK):
        raise argparse.ArgumentTypeError(f"{path} is not executable")
    return Path(path)


def available(path):
    """
    Check if a path is available to write to
    :param path: Path to check
    :return: Available path as a string
    """
    path = Path(path)

    if not (path.exists() and os.access(path, os.W_OK)):
        raise argparse.ArgumentTypeError(f"""{path} is either not writeable or 
                                          the directory does not exist""")

    return path


def get_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=__doc__)

    parser.add_argument('-i', '--input', type=existent, action='store', dest='inputdir', metavar='INPUT_DIR',
                        required=True,
                        help='Path to input directory with data downloaded from NDA Study 1887 containing fmriresults01/ and results/ subfolders.')
    parser.add_argument('-b', '--bids', '-d', '--destination', type=available, action='store', dest='bidsdir',
                        metavar='BIDS_DIR', required=True,
                        help="Path to output the BIDS formatted directory.")
    parser.add_argument('-m', '--method', choices=['softlink', 'copy', 'move'], type=str, action='store',
                        dest='method', metavar='METHOD', required=True,
                        help="Choose a method by which you'd like the files mapped: \ncopy = Outputs copies to the destination BIDS directory. \nmove = Moves files (without creating a copy) to the destination BIDS directory. \nsoftlink = Create a softlink (a.k.a. symbolic link or symlink) between NDA files and the destination BIDS directory.")

    args = parser.parse_args()

    return args.inputdir.resolve(), args.bidsdir.resolve(), args.method


def main():
    # parse in the arguments
    inputdir, bidsdir, method = get_args()

    # check if the inputdir is correct
    if not (inputdir.joinpath('fmriresults01').exists() and inputdir.joinpath('results').exists()):
        raise FileNotFoundError(f"""{inputdir} does not contain fmriresults01/ and results/ subfolders.
                                Please make sure you are pointing to the correct input directory and try again.""")

    # raise error if platform is Windows and method is softlink
    if platform.system() == 'Windows' and method == 'softlink':
        raise ValueError(f"""Softlink is not supported on Windows. Please use copy or move instead.""")

    # create lists of modality agnostic files and subject directory paths
    mod_agnostic_files = [i for i in list(inputdir.joinpath('results').glob('*')) if not i.name.endswith('.zip')]
    subjdirs = list(inputdir.joinpath('fmriresults01').glob('sub-*'))

    if method not in ['softlink', 'copy', 'move']:
        raise ValueError(f"""{method} is not a valid method. This should never happen.""")

    for subjdir in subjdirs:
        if method == 'softlink':
            os.symlink(subjdir, bidsdir.joinpath(subjdir.name))
        elif method == 'copy':
            shutil.copytree(subjdir, bidsdir.joinpath(subjdir.name))
        elif method == 'move':
            shutil.move(subjdir, bidsdir.joinpath(subjdir.name))

    for mod_agnostic in mod_agnostic_files:
        if method == 'softlink':
            os.symlink(mod_agnostic, bidsdir.joinpath(mod_agnostic.name))
        elif method == 'copy':
            shutil.copy2(mod_agnostic, bidsdir.joinpath(mod_agnostic.name))
        elif method == 'move':
            shutil.move(mod_agnostic, bidsdir.joinpath(mod_agnostic.name))


if __name__ == "__main__":
    main()
