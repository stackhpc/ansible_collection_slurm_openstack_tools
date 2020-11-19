# Ansible Collection - stackhpc.slurm_tools

# Roles

## `stackhpc.slurm_tools.openhpc_tests`

Tests of MPI functionality on a Slurm-based OpenHPC cluster. It uses openmpi4 and Intel MPI with UCX - so Centos 8 / OpenHPC v2 are required. It installs software only on the login node hence `/opt` must be exported from a login node to all compute notes. Then run this role on that login node only.

Currently the role assumes there is a single Slurm partition, and tests all the nodes in that partition.

Tests (with corresponding tags) are:
- `pingpong`: Runs Intel MPI Benchmark's IMB-MPI1 pingpong between a pair of (scheduler-selected) nodes. Reports zero-size message latency and maximum bandwidth.
- `pingmatrix`: Runs a similar pingpong test but between all pairs of nodes. Reports zero-size message latency & maximum bandwidth.
- `hpl-solo`: Runs HPL **separately** on all nodes, using 80% of memory, reporting Gflops on each node. **NB:** Set `openhpc_hpl_NB` as described below.

Role variables are:
- `openhpc_tests_hpl_NB`: Optional, default `192`. The HPL block size "NB" - for Intel CPUs see [here](https://software.intel.com/content/www/us/en/develop/documentation/mkl-linux-developer-guide/top/intel-math-kernel-library-benchmarks/intel-distribution-for-linpack-benchmark/configuring-parameters.html).
- `openhpc_tests_ucx_net_devices`: Optional, default `all`. Control which network device/interface to use, e.g. `mlx5_1:0`, as per `UCX_NET_DEVICES` ([docs](https://github.com/openucx/ucx/wiki/UCX-environment-parameters#setting-the-devices-to-use)). Note the default is probably not what you want.
