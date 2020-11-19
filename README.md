# Ansible Collection - stackhpc.slurm_tools

Included roles:
- `stackhpc.slurm_tools.openhpc_tests`: Test MPI functionality on an OpenHPC cluster. TODO: add proper docs but basically:
    - Export `/opt` from the login node to the compute nodes e.g. using our NFS role.
    - Run this role on the login node.
    - Available tags are:
        - `pingpong`: Run Intel MPI Benchmark's IMB-MPI1 pingpong between a pair of scheduler-selected nodes. Reports zero-size message latency and maximum bandwidth.
        - `pingmatrix`: Run a similar pingpong test but between all nodes. Reports zero-size message latency & maximum bandwidth. TODOs:
            - Provide output in matrix form.
            - Describe source and difference from IMB pingpong.
        - `hpl-solo`: Run HPL **separately** on all nodes, using 80% of memory. Reports Gflops.**NB:** Needs HPL block size "NB" setting as variable `hpl_NB`.
