# Copyright (c) 2021 StackHPC Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# NB: To test this from the repo root run:
#   ansible-playbook -i tests/inventory -i tests/inventory-mock-groups tests/filter.yml

from ansible import errors
import jinja2
import re
import subprocess
import json

REQUIRED_INSTANCE_ATTRS=('flavor', 'image', 'keypair', 'network')
REQUIRED_GROUP_ATTRS=('ram_mb', 'sockets', 'cores_per_socket', 'threads_per_core')

def modify_autoscale_partitions(openhpc_slurm_partitions):
    """ Modify openhpc_slurm_partitions to add autoscaling information.
    
        For each group/partition this constructs an `extra_nodes` option using information from the `cloud_nodes` and `cloud_instances` options.

        NB: Assumes openstack CLI client is installed on the ansible controller.
        
        Args:
            openhpc_slurm_partitions: openhpc_slurm_partitions variable from stackhpc.openhpc role.
    """

    for part in openhpc_slurm_partitions:
        for group in part.get('groups', [part]):
            group_name = group.get('name', '<undefined>')
            
            if 'cloud_nodes' in group:
                if 'cloud_instances' not in group:
                    raise errors.AnsibleFilterError(f"`openhpc_slurm_partitions` group '{group_name}' specifies 'cloud_nodes' but is missing 'cloud_instances'.")
                missing_group_attrs = ', '.join(set(REQUIRED_GROUP_ATTRS).difference(group))
                if missing_group_attrs:
                    raise errors.AnsibleFilterError(f"`openhpc_slurm_partitions` group '{group_name}' specifies 'cloud_nodes' but is missing items: {missing_group_attrs}.")
                missing_instance_attrs = ', '.join(set(REQUIRED_INSTANCE_ATTRS).difference(group['cloud_instances']))
                if missing_instance_attrs:
                    raise errors.AnsibleFilterError(f"`openhpc_slurm_partitions` group '{group_name}' item 'cloud_instances' is missing items: {missing_instance_attrs}.")
                cloud_names = group['cloud_nodes']
                # TODO: check for cloud nodes overlapping real ones?
                
                features = ['%s=%s' % (k, v) for (k, v) in group['cloud_instances'].items()]
                cloud_nodes = {
                    'NodeName': cloud_names,
                    'State':'CLOUD',
                    'RealMemory': group['ram_mb'],
                    'Sockets': group['sockets'],
                    'CoresPerSocket': group['cores_per_socket'],
                    'ThreadsPerCore': group['threads_per_core'],
                    'Features': ','.join(features),
                }
                group['extra_nodes'] = group.get('extra_nodes', [])
                group['extra_nodes'].append(cloud_nodes)

    return openhpc_slurm_partitions

class FilterModule(object):

    def filters(self):
        return {
            'modify_autoscale_partitions': modify_autoscale_partitions,
        }
