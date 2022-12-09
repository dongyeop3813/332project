import tempfile

from ssh import createSSHClient, getFile, putFile, exec_command_blocking
from machine_info import MASTER_IP_ADDRESS, MASTER_PORT, WORKER_IP_ADDRESS, WORKER_PORTS

SBT_BIN = '/home/cyan/.sbt.bin'

def setup_master():
    # Compile the project on the master machine because there is no java on the ssh bridge machine.
    ssh = createSSHClient(MASTER_IP_ADDRESS, MASTER_PORT)
    exec_command_blocking(ssh, 'git clone https://github.com/seonghyun26/332project.git')
    exec_command_blocking(ssh, f'cd /home/cyan/332project && {SBT_BIN}/sbt "master/assembly"')
    exec_command_blocking(ssh, f'cd /home/cyan/332project && {SBT_BIN}/sbt "worker/assembly"')
    exec_command_blocking(ssh, f'mv /home/cyan/332project/master/target/scala-2.12/master.jar /home/cyan/master.jar')
    exec_command_blocking(ssh, f'mv /home/cyan/332project/worker/target/scala-2.12/worker.jar /home/cyan/worker.jar')

def setup_workers():
    client = createSSHClient(MASTER_IP_ADDRESS, MASTER_PORT)
    with tempfile.TemporaryDirectory() as tempdir:
        getFile(client, '/home/cyan/worker.jar', f'{tempdir}/worker.jar')
        client.close()
        for port in WORKER_PORTS:
            client = createSSHClient(WORKER_IP_ADDRESS, port)
            putFile(client, f'{tempdir}/worker.jar', '/home/cyan/worker.jar')
            putFile(client, '/home/cyan/332project/script/multi-machine/worker.py', '/home/cyan/worker.py')
            client.close()

def setup_machines():
    setup_master()
    setup_workers()
