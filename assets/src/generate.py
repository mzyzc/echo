#!/usr/bin/env python3

"""
This script is part of the Echo secure messenger project
It is used to generate diagrams and graphs from Mermaid text files en masse
Mermaid source files should be in the same directory as this script
The images will be generated one directory above
"""

import os

initial_dir = os.getcwd()
final_dir = os.path.dirname(initial_dir)

for filename in os.listdir(initial_dir):
    if filename.endswith('.mmd'):
        initial_file = os.path.join(initial_dir, filename)
        final_file = os.path.join(final_dir, filename.replace('.mmd', '.png'))
        os.system(f'mmdc -i {initial_file} -o {final_file}')
