Role Name
=========

Installs python-based tools from https://github.com/stackhpc/slurm-openstack-tools.git into `/opt/slurm-tools/bin/`

Requirements
------------

Role Variables
--------------

None.

Dependencies
------------

Example Playbook
----------------

    - hosts: compute
      tasks:
        - import_role:
            name: stackhpc.slurm_openstack_tools.pytools
        

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
