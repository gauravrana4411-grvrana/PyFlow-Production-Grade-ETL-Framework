from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time


class FileHandler(FileSystemEventHandler):

    def on_created(self, event):
        print(f"New file detected: {event.src_path}")


def start_watcher(path: str):
    event_handler = FileHandler()

    observer = Observer()
    observer.schedule(
        event_handler,
        path,
        recursive=False
    )

    observer.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()
        observer.join()