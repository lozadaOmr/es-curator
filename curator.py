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

import os
import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.pycompat24 import get_exception


def main():

    module = AnsibleModule(
        argument_spec = dict(
            path   = dict(required=True, type='path'),
            config = dict(required=False, type='path')
        )
    )

    path = module.params['path']
    config = module.params['config']

     if not os.path.exists(path):
         module.fail_json(msg="Path %s not found" % (src))
     # if source is not yml file
     # module.fail_json(msg="Source %s not YAML" % (src))

    # use python to run "curator"
    # given src

if __name__ == '__main__':
    main()
