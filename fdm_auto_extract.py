import os
import time
import zipfile
import rarfile
import py7zr
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DownloadHandler(FileSystemEventHandler):
    def __init__(self, download_dir):
        self.download_dir = download_dir

    def on_created(self, event):
        # Only process files, not directories
        if event.is_directory:
            return
        
        # Wait briefly to ensure the file is completely downloaded
        time.sleep(1)
        
        file_path = event.src_path
        if file_path.endswith('.zip'):
            self.extract_zip(file_path)
        elif file_path.endswith('.rar'):
            self.extract_rar(file_path)
        elif file_path.endswith('.7z'):
            self.extract_7z(file_path)

    def extract_zip(self, file_path):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(self.download_dir)
            print(f'Extracted ZIP: {file_path}')

    def extract_rar(self, file_path):
        with rarfile.RarFile(file_path) as rar_ref:
            rar_ref.extractall(self.download_dir)
            print(f'Extracted RAR: {file_path}')

    def extract_7z(self, file_path):
        with py7zr.SevenZipFile(file_path, mode='r') as seven_zip:
            seven_zip.extractall(path=self.download_dir)
            print(f'Extracted 7Z: {file_path}')

def monitor_downloads(download_dir):
    event_handler = DownloadHandler(download_dir)
    observer = Observer()
    observer.schedule(event_handler, path=download_dir, recursive=False)
    observer.start()
    print(f'Monitoring downloads in {download_dir}...')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    download_directory = '/path/to/your/download/directory'  # Change this to your actual download path
    monitor_downloads(download_directory)