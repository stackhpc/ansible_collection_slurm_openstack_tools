stackhpc.slurm_openstack_tools.test
=========

Tests of MPI functionality on a Slurm-based OpenHPC cluster.

Currently the role assumes there is a single Slurm partition, and tests all the nodes in that partition.

Tests (with corresponding tags) are:
- `pingpong`: Runs Intel MPI Benchmark's IMB-MPI1 pingpong between a pair of (scheduler-selected) nodes. Reports zero-size message latency and maximum bandwidth.
- `pingmatrix`: Runs a similar pingpong test but between all pairs of nodes. Reports zero-size message latency & maximum bandwidth.
- `hpl-solo`: Runs HPL **separately** on all nodes, using 80% of memory, reporting Gflops on each node. **NB:** Set `openhpc_tests_hpl.NB` as described below.

Requirements
------------

- Requires a Centos 8 / OpenHPC v2 -based cluster as it uses the Openmpi4 package with UCX provided by v2 and requires `dnf`.
- A filesystem shared across the cluster.
- `slurm-libpmi-ohpc` to be installed on all nodes

Role Variables
--------------

- `openhpc_tests_rootdir`: Required, path to directory to use for root of tests. This must be an absolute path and must be on a cluster shared filesystem. Directory will be created if missing. Test software will be installed in a chroot `installs/` subdirectory.
- `openhpc_tests_hpl_NB`: Optional, default `192`. The HPL block size "NB" - for Intel CPUs see [here](https://software.intel.com/content/www/us/en/develop/documentation/mkl-linux-developer-guide/top/intel-math-kernel-library-benchmarks/intel-distribution-for-linpack-benchmark/configuring-parameters.html).
- `openhpc_tests_hpl_mem_frac`: Optional, default `0.8`. The HPL problem size "N" will be selected to target using this fraction of each node's memory.
- `openhpc_tests_ucx_net_devices`: Optional, default `all`. Control which network device/interface to use, e.g. `mlx5_1:0`, as per `UCX_NET_DEVICES` ([docs](https://github.com/openucx/ucx/wiki/UCX-environment-parameters#setting-the-devices-to-use)). Note the default is probably not what you want.
- `openhpc_tests_nodes`: Optional. A Slurm node expression, e.g. "compute-[0-15,19]" defining the nodes to use. If not set all nodes in the default partition are used.

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------
  - hosts: all
    name: Install slurm-libpmi-ohpc
    tasks:
      - yum:
          name: slurm-libpmi-ohpc
  - hosts: cluster_login[0]
    name: Run tests
    tasks:
      - import_role:
          name: stackhpc.slurm_tools.openhpc_tests
        vars:
          openhpc_tests_rootdir: /mnt/nfs/ohcp-tests
    

License
-------

Apache-2.0


Author Information
------------------

