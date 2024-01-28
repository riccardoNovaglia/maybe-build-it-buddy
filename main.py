import argparse

import watcher
from command_runner import CommandRunner

parser = argparse.ArgumentParser(description='Watch file changes and run a command.')
parser.add_argument('command',
                    type=str,
                    help='The command to be executed')
parser.add_argument('files',
                    type=str,
                    nargs='+',
                    help='The files to be watched')

parser.add_argument('hash_path',
                    type=str,
                    help='Where to store the files hashes')

args = parser.parse_args()

if __name__ == "__main__":
    command_runner = CommandRunner(args.command)
    command_runner.run_command()

    event_handler = watcher.HashFileChangeHandler(
        on_change=command_runner.run_command,
        hash_path=args.hash_path
    )
    event_handler.run_if_required(args.files)

    file_watcher = watcher.FileWatcher(args.files, event_handler)
    file_watcher.start_observing()
