FROM python:3.9-slim

RUN pip install prometheus-client docker

COPY jupyterhub_notebook_files_metrics.py /app/jupyterhub_notebook_files_metrics.py

CMD ["python", "/app/jupyterhub_notebook_files_metrics.py"]