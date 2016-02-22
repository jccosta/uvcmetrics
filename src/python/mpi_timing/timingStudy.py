import subprocess, pdb, time, sys, os
from config import *
DIRSIZE = sys.argv[1]
NFSHOME = os.environ['NFSHOME']
TIMING_PATH = NFSHOME + '/uvcmetrics/src/python/mpi_timing/'
SLURM_OUTPUTDIR = NFSHOME + '/slurm_output/' + DIRSIZE + '/'
RUNS = [1,2,3,4]
for (N,n,wait_time) in config:
    SBATCH_EXEC = 'sbatch --nodes=' + str(N) + ' --ntasks-per-node=' + str(n) + ' ' + TIMING_PATH +'diag_big.sh'
    print SBATCH_EXEC
    for run in RUNS:
        #SBATCH_EXEC = 'sbatch --nodes=1 --ntasks-per-node=6 diag.sh'
        slurm_output_file = SLURM_OUTPUTDIR + 'run_'+ str(N) +'_' + str(n) + '_' + str(run)
        os.environ['SLURMOUTPUT'] = slurm_output_file
        proc=subprocess.Popen([SBATCH_EXEC], shell=True, stdout=subprocess.PIPE)
        time.sleep(wait_time*60)
        #pdb.set_trace()
        #subprocess.Popen.wait(proc) #x.wait()
        #retrieve jobid and create the slurm file name
