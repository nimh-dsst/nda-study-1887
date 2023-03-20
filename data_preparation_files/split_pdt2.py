#!/usr/local/bin/python3
"""
Add program description here.
"""
import argparse
import subprocess
from collections import defaultdict
from pathlib import Path

from bids import BIDSLayout


def get_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=__doc__)

    parser.add_argument('-i', '--input', type=Path, action='store', dest='inputdir', metavar='INPUT_DIR',
                        help='Path to input BIDS directory.')
    parser.add_argument('-out', '--output', type=Path, action='store', dest='outdir', metavar='OUTPUT_DIR',
                        default=Path('.'), help="Path to directory that'll contain the outputs.")
    parser.add_argument('-e', '--even-numbered-runs', type=str, action='store', dest='even', metavar='EVEN_RUN_IDX',
                        choices=['PDw', 'T2w'], required=True,
                        help="Suffix associated with even numbered indices of PDT2 scans' 'run' entity.")
    parser.add_argument('-o', '--odd-numbered-runs', type=str, action='store', dest='odd', metavar='ODD_RUN_IDX',
                        choices=['PDw', 'T2w'], required=True,
                        help="Suffix associated with odd numbered indices of PDT2 scans' 'run' entity.")
    args = parser.parse_args()
    if args.outdir is None:
        args.outdir = args.inputdir

    return args.inputdir.resolve(), args.outdir.resolve(), args.even, args.odd


def run(cmdstr, logfile):
    """Runs the given command str as shell subprocess. If logfile object is provided, then the stdout and stderr of the
    subprocess is written to the log file.
    :param str cmdstr: A shell command formatted as a string variable.
    :param io.TextIOWrapper logfile: optional, File object to log the stdout and stderr of the subprocess.
    """
    if not logfile:
        subprocess.run(cmdstr, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf8', shell=True)
    else:
        subprocess.run(cmdstr, stdout=logfile, stderr=subprocess.STDOUT, encoding='utf8', shell=True)


def costruct_renaming_cmds(bids_files, suffix, layout):
    cmds_list = []
    req_fname_pattern = "sub-{subject}_ses-{session}_acq-{acquisition}_run-0{run}_{suffix}.{extension}"

    for idx, bids_file in enumerate(bids_files):
        req_files = [bids_file]
        req_files.extend(bids_file.get_associations())  # finds the corresponding json file

        for f in req_files:
            # path to parent dir of the file
            parent_dir = Path(f.dirname)

            # use existing entities dict to create the new filename
            new_entities = f.get_entities()
            new_entities['run'] = idx + 1
            new_entities['suffix'] = suffix

            # build bids filepath and extract filename only
            new_fname = Path(layout.build_path(new_entities, req_fname_pattern, validate=False)).name
            cmds_list.append(f"mv {f.path} {parent_dir.joinpath(new_fname)};")
    return cmds_list


def split_pdt2(pdt2_dict, even_suffix, odd_suffix, layout):
    renaming_cmds = []
    for subj_id in pdt2_dict.keys():
        for sess_id in pdt2_dict[subj_id].keys():
            even_runs = [s for s in pdt2_dict[subj_id][sess_id] if s.get_entities()['run'] % 2 == 0]
            # construct renaming commands for even numbered runs of PDT2 scans
            renaming_cmds.extend(costruct_renaming_cmds(even_runs, even_suffix, layout))

            odd_runs = [s for s in pdt2_dict[subj_id][sess_id] if s.get_entities()['run'] % 2 != 0]
            # construct renaming commands for odd numbered runs of PDT2 scans
            renaming_cmds.extend(costruct_renaming_cmds(odd_runs, odd_suffix, layout))

    # run the renaming commands
    print(f"Renaming {len(renaming_cmds)} files.")
    logfile = open('split_pdt2.log', 'w')
    for cmd in renaming_cmds:
        logfile.flush()
        logfile.write(cmd + '\n')
        run(cmd, logfile)
        logfile.write('******\n')


def main():
    input, output, even, odd = get_args()

    # create bids layout object 
    bids_layout = BIDSLayout(input)
    pdt2s = bids_layout.get(suffix='PDT2', extension='nii.gz')  # find all PDT2 image files

    # create a dict mapping subject-session to scan
    pdt2s_dict = defaultdict(lambda: defaultdict(list))
    for pdt2 in pdt2s:
        entities = pdt2.get_entities()
        pdt2s_dict[entities['subject']][entities['session']].append(pdt2)

    split_pdt2(pdt2s_dict, even, odd, bids_layout)

    return None


if __name__ == "__main__":
    main()
