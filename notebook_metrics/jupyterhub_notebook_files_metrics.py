# jupyterhub_notebook_files_metrics.py

from prometheus_client import start_http_server, Gauge
import docker
import time
import os
import re
import logging


logging.basicConfig(level=logging.INFO)


NOTEBOOK_FILE_SIZE = Gauge('jupyterhub_notebook_file_size_bytes', 'Size of individual notebook files', ['user', 'filename'])

def get_notebook_files_sizes():
    client = docker.from_env()
    for container in client.containers.list():
        if 'jupyter-' in container.name: 
            username = container.name.split('-')[-1]
            try:

                exit_code, output = container.exec_run(
                    "find /home/jovyan/work -type f -name '*.ipynb' -printf '%s\t%f\n'"
                )
                if exit_code == 0 and output.decode().strip():
                    lines = output.decode().splitlines()
                    for line in lines:
                        parts = line.strip().split('\t')
                        if len(parts) == 2:
                            size = int(parts[0])
                            filename = parts[1]

                            if not filename.endswith('-checkpoint.ipynb'):
                                NOTEBOOK_FILE_SIZE.labels(user=username, filename=filename).set(size)
                else:
                    logging.info(f"No notebooks found for user {username}")
            except Exception as e:
                logging.error(f"Error getting notebook file sizes for {username}: {e}")

if __name__ == '__main__':

    start_http_server(8085) 
    while True:
        get_notebook_files_sizes()
        time.sleep(60) 
