from nativeauthenticator import NativeAuthenticator
from dockerspawner import DockerSpawner
from prometheus_client import start_http_server

c.JupyterHub.authenticator_class = NativeAuthenticator
c.JupyterHub.spawner_class = DockerSpawner
c.JupyterHub.log_level = 'DEBUG'
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.spawner = DockerSpawner
c.JupyterHub.db_url = 'sqlite:///data/jupyterhub.sqlite'

c.DockerSpawner.network_name = 'jupyter-network'
c.DockerSpawner.remove = True
c.DockerSpawner.volumes = {"jupyterhub-user-{username}": "/home/jovyan/work"}
c.Spawner.notebook_dir = "/home/jovyan/work"
c.DockerSpawner.image = "jupyter/minimal-notebook:latest"

c.GenericOAuthenticator.enable_auth_state = True

#c.Authenticator.allowed_users = set()

c.Authenticator.admin_users = {'zmcadmin'}

c.NativeAuthenticator.open_signup = True
c.Authenticator.allow_all = True
c.Spawner.start_timeout = 120 

# Включение метрик Prometheus
c.JupyterHub.metrics_enabled = True

c.JupyterHub.prometheus_port = 8083

start_http_server(8083)