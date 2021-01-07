stackhpc.slurm_openstack_tools.test
=========

Tests of MPI functionality on a Slurm-based OpenHPC cluster. Currently it assumes there is a single Slurm partition, and tests some or all of the nodes in that partition.

Tests (with corresponding tags) are:
- `pingpong`: Runs Intel MPI Benchmark's IMB-MPI1 pingpong between a pair of (scheduler-selected) nodes. Reports zero-size message latency and maximum bandwidth.
- `pingmatrix`: Runs a similar pingpong test but between all pairs of nodes. Reports zero-size message latency & maximum bandwidth.
- `hpl-solo`: Runs HPL **separately** on all nodes, using 80% of memory, reporting Gflops on each node. **NB:** Set `openhpc_tests_hpl.NB` as described below.
- `hpl-all`: Runs HPL on all nodes, using 80% of memory, reporting total Gflops. **NB:** Set `openhpc_tests_hpl.NB` as described below.

See ansible output for summarised results and paths to detailed results files.

Note this role is intended as a post-deployment test for a cluster to which you have root access - it should **not** be used on a system running production jobs as they are likely to get broken by the reconfiguration it does. For repeatability with minimal impact on compute nodes it installs the packages required for the tests onto a login node, then exports that node's `/opt` to all other nodes in the play over NFS. This mount is reversed when the tests complete but see the "Cleanup" section below for limitations.

Requirements
------------

- A Centos 8 / OpenHPC v2 -based cluster as it uses the Openmpi4 package with UCX provided by v2.
- The `slurm-libpmi-ohpc` package installed on all nodes (done by default by `stackhpc.openhpc` galaxy role).
- A filesystem shared across the cluster and writeable from all nodes.

Role Variables
--------------

- `openhpc_tests_rootdir`: Required, path to directory to use for root of tests. Must be on a cluster shared filesystem writeable from all nodes. Directory will be created if missing.
- `openhpc_slurm_login`: Required, inventory name for login node to use.
- `openhpc_tests_hpl_NB`: Optional, default `192`. The HPL block size "NB" - for Intel CPUs see [here](https://software.intel.com/content/www/us/en/develop/documentation/mkl-linux-developer-guide/top/intel-math-kernel-library-benchmarks/intel-distribution-for-linpack-benchmark/configuring-parameters.html).
- `openhpc_tests_hpl_mem_frac`: Optional, default `0.8`. The HPL problem size "N" will be selected to target using this fraction of each node's memory.
- `openhpc_tests_ucx_net_devices`: Optional, default `all`. Control which network device/interface to use, e.g. `mlx5_1:0`, as per `UCX_NET_DEVICES` ([docs](https://github.com/openucx/ucx/wiki/UCX-environment-parameters#setting-the-devices-to-use)). Note the default is probably not what you want.
- `openhpc_tests_nodes`: Optional. A Slurm node expression, e.g. "compute-[0-15,19]" defining the nodes to use. If not set all nodes in the default partition are used.

Dependencies
------------

- `stackhpc.nfs` >= v20.11.1 (needs client mount state option)

Example Playbook
----------------

  - hosts: all
    tasks:
      - import_role:
          name: stackhpc.slurm_openstack_tools.test
        vars:
          openhpc_tests_rootdir: /mnt/nfs/ohcp-tests
          openhpc_tests_hpl_NB: 192
          openhpc_slurm_login: "{{ groups['cluster_login'] | first }}"

Cleanup
-------
At the end of the play:
- On the compute nodes `/opt` is unmounted and the fstab entry removed.
- On the login node the `/opt` export is removed.

However the following are left as-is as they may not have been changed by this role:
- Installs of test packages on the login node.
- Installs of NFS packages.
- NFS services are left running

License
-------

Apache-2.0


Author Information
------------------

