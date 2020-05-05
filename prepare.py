import json
import os
import sys
import glob
import zipfile
import argparse

parser = argparse.ArgumentParser(description='Unzip and find optimizer Python file + create config.json')
parser.add_argument('-i', '--input', help='Input path', required=True)
parser.add_argument('-o', '--output', help='Output path', required=True)
args = vars(parser.parse_args())

for path in glob.glob(os.path.join(args['input'], '*.zip')):
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(args['output'])

default_optimizer_path = os.path.join(args['output'], 'optimizer.py')

optimizer_py = None
if os.path.isfile(default_optimizer_path):
    optimizer_py = 'optimizer.py'
else:
    for path in glob.glob(os.path.join(args['output'], '*.py')):
        optimizer_py = os.path.basename(path)

if optimizer_py:
    config = {
        "BlackBoxOptimizer": [
            optimizer_py,
            {}
        ]
    }
    with open(os.path.join(args['output'], 'config.json'), 'w') as outfile:
        json.dump(config, outfile)
else:
    sys.exit(os.EX_NOINPUT)
