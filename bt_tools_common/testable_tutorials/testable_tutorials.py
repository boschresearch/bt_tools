# Copyright (c) 2024 - for information on the respective copyright owner
# see the NOTICE file

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This takes tutorials written in markdown files and extracts the code blocks
to be tested. The code blocks are then executed and the output is compared
to the expected output.
"""

import os
import re
import sys
import logging
import subprocess
import argparse
import select
from typing import Optional, List, Tuple

BLOCK_DELIM = '```'

class ROSTerminal:
    """
    Class for interacting with a ROS terminal
    """
    def __init__(self):
        self.process = subprocess.Popen(
            ['bash'], 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1)

    def execute(self, command: str) -> str:
        """
        Executes a command in the terminal
        """
        if not command.endswith('\n'):
            command += '\n'
        self.process.stdin.write(command)
        self.process.stdin.flush()

        output = []
        # Read the output
        while True:
        # Use select to wait for data to be available on stdout
            rlist, _, _ = select.select([self.process.stdout], [], [], 2.0)

            if self.process.stdout in rlist:
                line = self.process.stdout.readline().strip()
                print(line)
                if line:
                    output.append(line)
                else:
                    break
            else:
                break
        while True:
        # Use select to wait for data to be available on stdout
            rlist, _, _ = select.select([self.process.stdout], [], [], 2.0)

            if self.process.stdout in rlist:
                line = self.process.stdout.readline().strip()
                print(line)
                if line:
                    output.append(line)
                else:
                    break
            else:
                break

        error = []
        # Read the error
        while True:
        # Use select to wait for data to be available on stderr
            rlist, _, _ = select.select([self.process.stderr], [], [], 2.0)

            if self.process.stderr in rlist:
                line = self.process.stderr.readline().strip()
                print(line)
                if line:
                    error.append(line)
                else:
                    break
            else:
                break

        if error:
            logging.error(f'Error: {error}')
        return output
        
    def close(self):
        """
        Closes the terminal
        """
        self.process.stdin.close()
        self.process.stdout.close()
        self.process.stderr.close()
        self.process.kill()

def extract_code_blocks(file_path: str) -> List[Tuple[str, str]]:
    """
    Extracts code blocks from a markdown file
    """
    code_blocks: List[Tuple[str, str]] = []  # (language, code)
    with open(file_path, 'r') as file:
        code: Optional[str] = None
        language: Optional[str] = None
        in_code_block: bool = False
        for line in file:
            if line.startswith(BLOCK_DELIM):
                new_language = line.strip(BLOCK_DELIM).strip()
                if len(new_language) == 0:  # end of code block
                    code_blocks.append((language, code))
                    code = None
                    language = None
                    in_code_block = False
                else:
                    language = new_language
                    code = ''
                    in_code_block = True
            elif in_code_block:
                if code is not None:
                    code += line
    return code_blocks

def run_code_blocks(code_blocks: List[Tuple[str, str]]):
    """
    Runs the code blocks
    """
    terminal = ROSTerminal()
    terminal.execute('source /opt/ros/humble/setup.bash')
    for language, code in code_blocks:
        if language == 'bash':
            for line in code.split('\n'):
                if len(line.strip()) == 0:
                    continue
                logging.info(f'cmd: {line}')
                output = terminal.execute(line)
                logging.info(f'out: {output}')
        else:
            logging.warning(f'Unsupported language: {language}')
    terminal.close()

def main():
    """
    Main function
    """
    logging.basicConfig(level=logging.INFO)
    ap = argparse.ArgumentParser()
    ap.add_argument('file', help='Markdown file to extract code blocks from')
    args = ap.parse_args()
    code_blocks = extract_code_blocks(args.file)
    print(code_blocks)
    run_code_blocks(code_blocks)

if __name__ == '__main__':
    main()