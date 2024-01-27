import subprocess


class CommandRunner:
    def __init__(self, cmd: str):
        self.cmd = cmd

    def run_command(self):
        subprocess.run(self.cmd, shell=True)
