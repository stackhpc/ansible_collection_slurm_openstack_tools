stackhpc.slurm_openstack_tools.test
=========

Tests of MPI functionality on a Slurm-based OpenHPC cluster.

Currently the role assumes there is a single Slurm partition, and tests all the nodes in that partition.

Tests (with corresponding tags) are:
- `pingpong`: Runs Intel MPI Benchmark's IMB-MPI1 pingpong between a pair of (scheduler-selected) nodes. Reports zero-size message latency and maximum bandwidth.
- `pingmatrix`: Runs a similar pingpong test but between all pairs of nodes. Reports zero-size message latency & maximum bandwidth.
- `hpl-solo`: Runs HPL **separately** on all nodes, using 80% of memory, reporting Gflops on each node. **NB:** Set `openhpc_hpl_NB` as described below.

Requirements
------------

- Requires a Centos 8 / OpenHPC v2 -based cluster as it uses the Openmpi4 package with UCX provided by v2.
- `/opt` must be exported from a login node to all compute notes, as software is only installed on the login node. TODO: maybe role should do that and undo it?
- A filesystem shared across the cluster.

Role Variables
--------------

- `openhpc_tests_rootdir`: Required, path to directory to use for root of tests. Must be on a cluster shared filesystem. Directory will be created if missing.
- `openhpc_tests_hpl_NB`: Optional, default `192`. The HPL block size "NB" - for Intel CPUs see [here](https://software.intel.com/content/www/us/en/develop/documentation/mkl-linux-developer-guide/top/intel-math-kernel-library-benchmarks/intel-distribution-for-linpack-benchmark/configuring-parameters.html).
- `openhpc_tests_ucx_net_devices`: Optional, default `all`. Control which network device/interface to use, e.g. `mlx5_1:0`, as per `UCX_NET_DEVICES` ([docs](https://github.com/openucx/ucx/wiki/UCX-environment-parameters#setting-the-devices-to-use)). Note the default is probably not what you want.
- `openhpc_tests_nodes`: Optional. If set, only run jobs on these nodes, otherwise all nodes in first partition shown by `sinfo` will be used. Takes a slurm node expression, e.g. "compute-[0-15,19]".

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

  - hosts: cluster
    name: Export/mount /opt via NFS for ohcp and intel packages
    become: yes
    tasks:
      - import_role:
          name: ansible-role-cluster-nfs
        vars:
          nfs_enable:
            server:  "{{ inventory_hostname in groups['cluster_login'] | first }}"
            clients: "{{ inventory_hostname in groups['cluster_compute'] }}"
          nfs_server: "{{ hostvars[groups['cluster_login'] | first ]['server_networks']['ilab'][0] }}"
          nfs_export: "/opt"
          nfs_client_mnt_point: "/opt"
          
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

