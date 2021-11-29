# Ansible Collection - stackhpc.slurm_tools

Tools to add functionality to a Slurm-based OpenHPC cluster on OpenStack created by `stackhpc.openhpc`.

## Roles

- `stackhpc.slurm_openstack_tools.test`: Test MPI functionality - [README](roles/test/README.md)
- `stackhpc.slurm_openstack_tools.rebuild`: Add Slurm-controled rebuild/reimage capability - [README](roles/rebuild/README.md).
- `stackhpc.slurm_openstack_tools.pytools`: Add python utilities used by other roles - [README](roles/pytools/README.md).
- `stackhpc.slurm_openstack_tools.slurm-stats`: Configures a tool to transform `sacct` output for import into elasticsearch/loki - [README](roles/slurm-stats/README.md).
- `stackhpc.slurm_openstack_tools.autoscale`: Add Slurm autosacling functionality - [README](roles/autoscale/README.md).