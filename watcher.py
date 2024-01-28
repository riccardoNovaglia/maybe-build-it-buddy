import hashlib
import os
from os import path

import watchdog
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class FileWatcher:
    def __init__(self, files: list[str], event_handler: FileSystemEventHandler):
        self.files = files

        self.observer = Observer()
        for file in self.files:
            if os.path.exists(file):
                self.observer.schedule(
                    event_handler,
                    file,
                    True
                )
            else:
                print(f"Warning: File '{file}' does not exist.")

    def start_observing(self):
        self.observer.start()
        try:
            while self.observer.is_alive():
                self.observer.join(1)
        except KeyboardInterrupt:
            print("Bye")
        finally:
            self.observer.stop()
            self.observer.join()


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, on_change: callable):
        self.on_change = on_change

    def dispatch(self, event):
        super().dispatch(event)

    def on_modified(self, event):
        self.on_change()


class HashFileChangeHandler(FileChangeHandler):
    def __init__(self, on_change: callable, hash_path: str):
        super().__init__(on_change)
        self.hash_path = path.abspath(hash_path)

        initial_content = open(self.hash_path, 'r+').read()
        self.hashes = initial_content.splitlines()

        self.hashes_file = open(self.hash_path, 'w+')
        self.hashes_file.write(initial_content)
        self.hashes_file.flush()

    def on_modified(self, event: watchdog.events.FileSystemEvent):
        super().on_modified(event)
        self.update_hash(event.src_path)

    def _file_hash_index(self, file_path: str) -> int:
        for i, line in enumerate(self.hashes):
            if f"{file_path} " in line:
                return i
        return -1

    def update_hash(self, changed_path: str):
        file_hash = self._get_expected_hash(changed_path)

        file_hash_index = self._file_hash_index(changed_path)
        if file_hash_index == -1:
            self.hashes.append(file_hash)
        else:
            self.hashes[file_hash_index] = file_hash

        self._write_hashes()

    def _write_hashes(self):
        self.hashes_file.seek(0)
        self.hashes_file.writelines(self.hashes)
        self.hashes_file.flush()

    def _get_expected_hash(self, file_path):
        file_hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
        return f"{file_path} {file_hash}\n"

    def run_if_required(self, files: list[str]):
        for file in files:
            self.update_hash(file)
