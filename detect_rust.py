"""
Simulate the detection of rust.
"""

import json
import logging
import os
from pathlib import Path
import shutil
import sys
from time import sleep

LOG_FORMAT = '[%(levelname)s] %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=LOG_FORMAT)


def load_inputs(input_path):
    inputs_desc = json.load(open(input_path))
    inputs = inputs_desc.get('inputs')
    parameters = inputs_desc.get('parameters')
    return inputs, parameters


def main():
    SCRIPT_DIR = Path(__file__).parent.resolve()
    WORKING_DIR = os.getenv('DELAIRSTACK_PROCESS_WORKDIR')
    if not WORKING_DIR:
        raise KeyError('DELAIRSTACK_PROCESS_WORKDIR environment variable must be defined')
    WORKING_DIR = Path(WORKING_DIR).resolve()

    logging.debug('Extracting inputs and parameters...')

    # Retrieve inputs and parameters from inputs.json
    inputs, parameters = load_inputs(WORKING_DIR / 'inputs.json')

    # Use the 'detection-mode' parameter to define the sleep time between log entries
    detection_mode = parameters.get('detection-mode')
    logging.info('Rust detection mode : {}'.format(detection_mode))

    if detection_mode == 'Fast':
        sleep_time = 2
    elif detection_mode == 'Standard':
        sleep_time = 5
    else:  # Deep
        sleep_time = 15

    # Get info for the 'building_mesh' input
    building_mesh = inputs.get('building_mesh')
    logging.info('Building mesh dataset: {name!r} (id: {id!r})'.format(
        name=building_mesh['name'],
        id=building_mesh['_id']))

    for component in building_mesh.get('components'):
        logging.debug('Component {name!r}: {path!r}'.format(
            name=component['name'],
            path=component['path'])
        )

    # Simulate computation
    logging.info('Computing rust detection...')
    for log_sample in ('Using very complex deep learning algorithms',
                       'Very very complex...',
                       'Rust patch found (medium severity)',
                       'Still computing...',
                       'Rust patch found (low severity)',
                       'Still computing...',
                       'Still computing...',
                       'Rust patch found (HIGH severity)'):
        logging.info(log_sample)
        sleep(sleep_time)

    logging.warning('3 issues found (1 high/1 medium/1 low)')

    # Create the PDF report
    logging.debug('Creating the PDF report')
    outpath = WORKING_DIR / 'report-sample.pdf'
    shutil.copyfile(SCRIPT_DIR / 'report-sample.pdf', outpath)
    
    # Create the outputs.json to describe the deliverable and its path
    logging.debug('Creating the outputs.json')
    output = {
        "outputs": {
            "rust-report": {  # Must match the name of deliverable in rust-detector.yaml
                "type": "file",
                "format": "pdf",
                "name": "Rust detection report",
                "components": [
                    {
                        "name": "file",
                        "path": str(outpath)
                    }
                ]
            }
        },
        "version": "0.1"
    }
    with open(WORKING_DIR / 'outputs.json', 'w+') as f:
        json.dump(output, f)

    logging.info('End of processing.')


if __name__ == '__main__':
    main()
