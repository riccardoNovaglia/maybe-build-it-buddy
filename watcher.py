import os

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
