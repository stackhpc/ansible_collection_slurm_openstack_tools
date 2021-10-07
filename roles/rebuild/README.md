stackhpc.slurm_openstack_tools.rebuild
=========

Enable the compute nodes of a Slurm-based OpenHPC cluster on Openstack to be reimaged from Slurm.

Once this role has been used with the `stackhpc.openhpc role`, node(s) can be reimaged by running the following from any Slurm node:

    scontrol reboot [ASAP] [nextstate=<RESUME|DOWN>] reason="rebuild image:<image_id>" [<NODES>]

where:
- `<image_id>` is the name (if unique) or ID of an image in OpenStack.
- `<NODES>` is a Slurm hostlist expression defining the nodes to reimage.
- `ASAP` means the rebuild will happen as soon as existing jobs on the node(s) complete - no new jobs will be scheduled on it.
- If `nextstate=...` is not given nodes remain in DRAIN state after the rebuild.

Requirements
------------

- An OpenHPC cluster created using the `stackhpc.openhpc` role. This role must be run before that role's `runtime.yml` playbook, as it modifies the `openhpc_config` variable.

Role Variables
--------------

- `openhpc_rebuild_clouds`: Optional, path to a `clouds.yaml` file containing a single cloud. Defaults to `~/.config/openstack/clouds.yaml`.
- `openhpc_enable.batch`: Set to `true` on compute nodes. Note this is the same variable as used in `stackhpc.openhpc` so will not need to be specifically set.
- `openhpc_rebuild_no_log`: Optional bool, default of true prevents contents of `openhpc_rebuild_clouds` from being logged.

It is recommended that the `openhpc_rebuild_clouds` is an [application credential](https://docs.openstack.org/keystone/latest/user/application_credentials.html). This can be created in Horizon via Identity > Application Credentials > +Create Application Credential. The usual role required is `member`. Using access rules has been found not to work at present. Note that the downloaded credential can be encrpyted using `ansible-vault` to allow commit to source control. It will automatically be decrypted when copied onto the compute nodes.

Dependencies
------------

The `stackhpc.openhpc` role.

Example Playbook
----------------

```yaml
- name: Setup slurm
  hosts: openhpc
  become: yes
  vars:
    openhpc_enable:
      batch: "{{ inventory_hostname in groups['cluster_compute'] }}"
    # NB: see stackpc.openhpc role for its other required vars
  tasks:
    - name: Validate application credential for rebuild
      import_role:
        name: stackhpc.slurm_openstack_tools.rebuild
        tasks_from: validate.yml
    - name: Setup slurm-driven reimage
      import_role:
        name: stackhpc.slurm_openstack_tools.rebuild
    - name: Create slurm cluster
      import_role:
        name: stackhpc.openhpc
```

License
-------

Apache-2.0

Author Information
------------------

StackHPC Ltd
