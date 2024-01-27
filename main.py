import argparse

from command_runner import CommandRunner
from watcher import FileChangeHandler, FileWatcher

parser = argparse.ArgumentParser(description='Watch file changes and run a command.')
parser.add_argument('command',
                    type=str,
                    help='The command to be executed')
parser.add_argument('files',
                    type=str,
                    nargs='+',
                    help='The files to be watched')

args = parser.parse_args()

if __name__ == "__main__":
    command_runner = CommandRunner(args.command)
    command_runner.run_command()

    event_handler = FileChangeHandler(on_change=command_runner.run_command)

    file_watcher = FileWatcher(args.files, event_handler)
    file_watcher.start_observing()
