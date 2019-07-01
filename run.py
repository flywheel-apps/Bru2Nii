#!/usr/bin/env python
import logging
import os
import re
import subprocess
import sys
import zipfile

import flywheel


log = logging.getLogger('flywheel:Bru2Nii')


if __name__ == '__main__':
    with flywheel.GearContext() as context:
        context.init_logging()
        context.log_config()

        input_filepath = context.get_input_path('bruker_file')
        input_filename = os.path.basename(input_filepath)
        with zipfile.ZipFile(input_filepath) as zf:
            zf.extractall(context.work_dir)

        cmd = [
            'Bru2', # CLI version of Bru2Nii
            '-v',   # verbose conversion comments
            '-f',   # force conversion of localizer images (multiple slice orientations)
            '-z',   # gz compress images (".nii.gz")
        ]
        if not context.config.get('scale_size'):
            cmd.append('-a')  # actual size (otherwise x10 scale so animals match humans)
        output_filename = re.sub(r'\.pv\d\.zip$', '', input_filename)
        output_filepath = os.path.join(context.output_dir, output_filename)
        cmd.extend([
            '-o', output_filepath,  # output filename(s) based on input filename (sans ext)
            context.work_dir,       # extracted bruker files (Bru2 finds acqp recursively)
        ])

        log.info('calling Bru2: %s', cmd)
        subprocess.check_call(cmd)

        nifti_outputs = os.listdir(context.output_dir)
        if not nifti_outputs:
            log.error('No NIfTI outputs created')
            sys.exit(1)

        for nifti in nifti_outputs:
            context.update_file_metadata(nifti, type='nifti', modality='MR')
