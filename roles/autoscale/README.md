# autoscale

Support autoscaling nodes on OpenStack clouds, i.e. creating nodes when necessary to service the queue and deleting them when they are no longer needed.

This is implemented using Slurm's ["elastic computing"](https://slurm.schedmd.com/elastic_computing.html) features. As these use Slurm's [power saving](https://slurm.schedmd.com/power_save.html) features it operates slightly differently than might be expected:
- Nodes can be defined as in a "CLOUD" state which means the Slurm controller does not expect to be able to contact them on startup.
- Having any CLOUD state nodes in the config enables powersaving globally for the cluster, although specific nodes can be excluded from powersaving.
- With powersaving enabled, Slurm will resume/add nodes as necessary to service jobs in the queue, and suspend/destroy them (after a configurable delay) when idle.
- All potential nodes in the cluster - including those in CLOUD state - must be defined in the Slurm configuration. The maximum size of the cluster is therefore fixed, and changing this requires a restart of all Slurm daemons.

By default, node creation and deletion will be logged in the control node's syslog.

This role should run on the Slurm control node only. Note some role variables are likely to need configuring.

## Requirements

- Working DNS.
- The OpenStack CLI client and active OpenStack credentials on localhost (e.g a sourced `openrc.sh` in the shell running ansible).
- Role `stackhpc.slurm_openstack_tools.pytools`. Installs [slurm-openstack-tools](github.com/stackhpc/slurm-openstack-tools) which provides a venv with the `openstacksdk` and the required resume/suspend scripts.
- Role `stackhpc.openhpc` to create a Slurm cluster.

## Role Variables

- `autoscale_clouds`: Optional, path to a `clouds.yaml` file containing a single cloud. Defaults to `~/.config/openstack/clouds.yaml`. It is recommended this is an [application credential](https://docs.openstack.org/keystone/latest/user/application_credentials.html). This can be created in Horizon via Identity > Application Credentials > +Create Application Credential. The usual role required is `member`. Using access rules has been found not to work at present. Note that the downloaded credential can be encrpyted using `ansible-vault` to allow it to be committed to source control. It will automatically be decrypted when copied onto the compute nodes.

The following variables are likely to need tuning for the specific site/instances:
- `autoscale_suspend_time`: Optional, default 120s. See `slurm.conf` parameter [SuspendTime](https://slurm.schedmd.com/archive/slurm-20.11.7/slurm.conf.html#OPT_SuspendTime).
- `autoscale_suspend_timeout`: Optional, default 30s. See `slurm.conf` parameter [SuspendTimeout](https://slurm.schedmd.com/archive/slurm-20.11.7/slurm.conf.html#OPT_SuspendTimeout).
- `autoscale_resume_timeout`: Optional, default 300s See `slurm.conf` parameter [ResumeTimeout](https://slurm.schedmd.com/archive/slurm-20.11.7/slurm.conf.html#OPT_ResumeTimeout).

The following variables may need altering for production:
- `autoscale_show_suspended_nodes`: Optional, default `true`. Whether to show suspended/powered-down nodes in `sinfo` etc. See `slurm.conf` parameter [PrivateData - cloud](https://slurm.schedmd.com/archive/slurm-20.11.7/slurm.conf.html#OPT_cloud).
- `autoscale_debug_powersaving`: Optional, default `true`. Log additional information for powersaving, see `slurm.conf` parameter [DebugFlags - PowerSave](https://slurm.schedmd.com/archive/slurm-20.11.7/slurm.conf.html#OPT_PowerSave_2).
- `autoscale_slurmctld_syslog_debug`: Optional, default `info`. Syslog logging level. See `slurm.conf` parameter [SlurmctldSyslogDebug](https://slurm.schedmd.com/archive/slurm-20.11.7/slurm.conf.html#OPT_SlurmctldSyslogDebug).
- `autoscale_suspend_exc_nodes`: Optional. List of nodenames (or Slurm hostlist expressions) to exclude from "power saving", i.e. they will not be autoscaled away. If running this role from the [Slurm appliance](https://github.com/stackhpc/ansible-slurm-appliance/) note that by default login-only nodes and non-CLOUD state nodes are automatically excluded from power saving.

## stackhpc.openhpc role variables
This role modifies what the [openhpc_slurm_partitions variable](https://github.com/stackhpc/ansible-role-openhpc#slurmconf) in the `stackhpc.openhpc` role accepts. Partition/group definitions may additionally include:
- `cloud_nodes`: Optional. Slurm hostlist expression (e.g. `'small-[8,10-16]'`) defining names of nodes to be defined in a ["CLOUD" state](https://slurm.schedmd.com/slurm.conf.html#OPT_CLOUD), i.e. not operational when the Slurm control daemon starts.

If `cloud_nodes` is defined for a partition/group, the following parameters **must** be defined for that partition/group:
- `cloud_instances`:  A mapping with keys `flavor`, `image`, `keypair` and `network` defining the OpenStack ID or names of properties for CLOUD-state nodes. If there is a port with a name matching the node name on the specified network then the created instance will be attached to this port, otherwise a new port is created. This permits CLOUD-state nodes to use predefined ports e.g. for non-default bindings or if DNS is not available.
- `ram_mb`: The physical RAM available in each server of this group ([slurm.conf](https://slurm.schedmd.com/slurm.conf.html#OPT_RealMemoryl) parameter `RealMemory`) in MiB, i.e. some fraction of value reported by `free --mebi`. By default the `stackhpc.openhpc` role uses a fraction of 0.95 (see role variable `openhpc_ram_multiplier`) although this may be slightly high for some circumstances.
- `sockets`: Number of sockets.
- `cores_per_socket`: Number of cores per socket.
- `threads_per_core`: Number of threads per core (physical or logical, as shown by e.g. `lscpu`).

Note that for non-CLOUD nodes, the memory and CPU parameters are set automatically by Ansible in the `stackhpc.openhpc` role from host facts. This implies that if a group (or partition if it does not contain groups) contains both CLOUD and non-CLOUD nodes, they must be homogenous in terms of processors and memory.

Note that currently monitoring is not enabled for CLOUD-state nodes.

# Dependencies

`stackhpc.openhpc` role. This role needs to run before tasks from `stackhpc.openhpc:runtime.yml` but requires the `slurm` user to be present. See example playbook below.

# Example Playbook

This role should be run on the Slurm controller only.

```yaml
  - hosts: control
    become: yes
    tasks:
      - name: Install Slurm packages to create slurm user
        import_role:
          name: stackhpc.openhpc
          tasks_from: install.yml
      - name: Setup autoscaling using OpenStack
        import_role:
          name: stackhpc.slurm_openstack_tools.autoscale
      - name: Setup Slurm
        import_role:
          name: stackhpc.openhpc
```

# License

Apache v2

# Author Information

StackHPC Ltd.
