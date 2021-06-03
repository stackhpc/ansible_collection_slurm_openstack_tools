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
- `openhpc_rebuild_reconfigure`: Optional bool, whether to reconfigure Slurm at the end of this role so `scontrol reboot ...` uses the new script. Default `true`.
- `openhpc_enable.batch`: Set to `true` on compute nodes. Note this is the same variable as used in `stackhpc.openhpc`.

It is recommended that the `openhpc_rebuild_clouds` is an [application credential](https://docs.openstack.org/keystone/latest/user/application_credentials.html). This can be created in Horizon via Identity > Application Credentials > +Create Application Credential. The usual role required is `member`. Access rules (if using Train or above) can be as below or similar:

```yaml
- service: compute
  method: POST
  path: /v2.1/servers
```

Note that the downloaded credential can be encrpyted using `ansible-vault` to allow commit to source control. It will automatically be decrypted when copied onto the compute nodes.

Dependencies
------------

The `stackhpc.openhpc` role.

Example Playbook
----------------

    - hosts: cluster
      name: Setup openstack rebuild script
      tags: rebuild
      become: true
      tasks:
        - import_role:
            name: stackhpc.slurm_openstack_tools.rebuild
          vars:
            openhpc_enable:
              batch: "{{ inventory_hostname in groups['cluster_compute'] }}"


License
-------

Apache-2.0

Author Information
------------------

StackHPC Ltd
