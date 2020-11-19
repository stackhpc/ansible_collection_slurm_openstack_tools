Role Name
=========

Enable the compute nodes of a Slurm-based OpenHPC cluster on Openstack to be reimaged from Slurm.

Once this playbook has run, from a Slurm node run:

    scontrol reboot [ASAP] reason="rebuild image:<image_id>" [<NODES>]

to rebuild the selected nodes with the given image. Note that:
- If "ASAP" is included, the rebuild will happen as soon as existing jobs on the node(s) complete - no new jobs will be scheduled on it
- If "reason" does not start with "rebuild" (or a node is not provisioned on Openstack) node(s) will simply reboot.
- If "image:<image_id>" is not specified the node(s) will be rebuilt with the existing image.

Requirements
------------

- An OpenHPC cluster created using the `stackhpc.openhpc` role.


Role Variables
--------------

- `openhpc_rebuild_clouds`: Optional, path to a `clouds.yaml` file containing a single cloud. Defaults to `~/.config/openstack/clouds.yaml`.
- `openhpc_rebuild_reconfigure`: Optional bool, whether to reconfigure Slurm at the end of this role so `scontrol reboot ...` uses the new script. Default `true`.
- `openhpc_enable.batch`: Set to `true` on compute nodes. Note this is the same variable as used in `stackhpc.openhpc`.


A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:



    - hosts: cluster
      name: Setup openstack rebuild script
      tags: rebuild
      become: true
      tasks:
        - import_role:
            name: stackhpc.slurm_tools.openhpc_rebuild
          vars:
            openhpc_enable:
              batch: "{{ inventory_hostname in groups['cluster_compute'] }}"


License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
