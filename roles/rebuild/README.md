stackhpc.slurm_openstack_tools.rebuild
=========

Enable the compute nodes of a Slurm-based OpenHPC cluster on Openstack to be reimaged from Slurm.

Once this playbook has run, from a Slurm node run:

    scontrol reboot [ASAP] [nextstate=<RESUME|DOWN>] reason="rebuild image:<image_id>" [<NODES>]

to rebuild the selected nodes with the given image. Note that:
- If "ASAP" is included, the rebuild will happen as soon as existing jobs on the node(s) complete - no new jobs will be scheduled on it
- If "reason" does not start with "rebuild" (or a node is not provisioned on Openstack) node(s) will simply reboot.
- If "image:<image_id>" is not specified the node(s) will be rebuilt with the existing image.
- Without "nextstate" nodes remain in DRAIN state after the rebuild.

Requirements
------------

- An OpenHPC cluster created using the `stackhpc.openhpc` role.

Role Variables
--------------

- `openhpc_rebuild_clouds`: Optional, path to a `clouds.yaml` file containing a single cloud. Defaults to `~/.config/openstack/clouds.yaml`.

Dependencies
------------

This role sets facts to control variables for the `stackhpc.openhpc` role, so it must be run in the same play and before that role. It only needs to run on the Slurm controller.

Example Playbook
----------------

    - hosts: control
      name: Setup openstack rebuild script
      tags: rebuild
      become: true
      tasks:
        - import_role:
            name: stackhpc.slurm_openstack_tools.rebuild
    
    - hosts: cluster
      name: configure slurm
      become: true
      tasks:
        import_role:
          name: stackhpc.openhpc
          ...


License
-------

Apache-2.0

Author Information
------------------

stackhpc.com
