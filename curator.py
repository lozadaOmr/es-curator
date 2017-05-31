#!/usr/bin/python
# encoding: utf-8

# (c) 2017, Omar Lozada <omrlozada@gmail.com>
#
# This file is part of Ansible
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADA = {'metadata_version': '1.0',
                  'status': ['preview'],
                  'supported_by': 'community'}


DOCUMENTATION = '''
---
module: curator
short_description: Executes a ACTION_FILE on remote node.
description:
    - The C(command) module takes the argument path to ACTION_FILE  on host.
version_added: "2.4"
author: "Omar Lozada (@lozadaOmr)"
options:
  path:
    description:
      - The complete path to the location of the action_file to be run.
    required: true
  config:
    description:
      - The complete path to the location of the curator.yml
      - This is optional and is assumed to be located at ~/.curator/curator.yml
'''

EXAMPLES = '''
- name: Run snapshot.yml on host
  curator:
    path: "/home/ubuntu/snapshot.yml"
    config: "/home/ubuntu/.curator/curator.yml"
'''

RETURN = '''
result:
    description: Return code curator call
    returned: success
    type: integer
    sample: 2
msg:
    description:
    returned: changed
    type: string
    sample: No such file or directory
'''

import os
import getpass

from subprocess import Popen
from distutils import spawn
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.pycompat24 import get_exception


def generate_command(data):
    cmd = []
    cmd.append('curator')

    if data.get('dry-run',None):
        cmd.append("--dry-run")

    if data.get('config', None):
        cmd.append("--config")
        cmd.append(data['config'])

    cmd.append(data['path'])
    return ' '.join(cmd)


def file_exist(data):

    if not os.path.exists(data):
        return False
    return True


def check_yaml_file(data):

    if not data.endswith('.yml'):
        return False
    return True


def get_default_config(pwd, module):

    pwd_path = os.path.dirname(pwd)

    try:
        os.chdir(pwd_path)
    except OSError as e:
        module.fail_json(msg=e.strerror + ' ' + pwd_path)

    if not file_exist(pwd):
        module.fail_json(msg="File does not exist")

    file_name = os.path.basename(pwd)

    if not check_yaml_file(file_name):
        module.fail_json(msg="File is not YAML")

    return file_name, pwd_path, pwd

def validate(pwd, module):

    pwd_path = os.path.dirname(pwd)

    try:
        os.chdir(pwd_path)
    except OSError as e:
        module.fail_json(msg=e.strerror)

    if not file_exist(pwd):
        module.fail_json(msg="File does not exist")

    file_name = os.path.basename(pwd)

    if not check_yaml_file(file_name):
        module.fail_json(msg="File is not YAML")

    return file_name, pwd_path, pwd


def main():

    module = AnsibleModule(
        argument_spec = dict(
            path   = dict(required=True, type='path'),
            config = dict(required=False, type='path'),
        ),
        supports_check_mode=True
    )

    path = module.params['path']
    config = module.params['config']

    data = {}

    if not path:
        module.fail_json(msg="Path is required")

    data['file_name'], data['file_dir'], data['path'] = validate(path, module)

    if config:
        data['config_name'], data['config_dir'], data['config'] = validate(config, module)
    else:
        # check if config exists in default home dir
        config = os.environ['HOME'] + '/.curator/curator.yml'
        data['config_name'], data['config_dir'], data['config'] = get_default_config(config, module)

    if module.check_mode:
        data['dry-run'] = True

    cmd = generate_command(data)

    curator_dir = spawn.find_executable("curator")

    if not curator_dir:
        module.fail_json(msg="curator: not found")

    try:
        proc = Popen(cmd, shell=True, cwd=data['file_dir'])
        proc.wait()
        module.exit_json(msg="Success", result=proc.returncode)
    except Exception:
        e = get_exception()
        module.fail_json(msg=e)


if __name__ == '__main__':
    main()
