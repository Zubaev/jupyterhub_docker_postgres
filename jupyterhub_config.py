from nativeauthenticator import NativeAuthenticator
from dockerspawner import DockerSpawner

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
c.DockerSpawner.image = "zms-notebook:latest"

c.GenericOAuthenticator.enable_auth_state = True

#c.Authenticator.allowed_users = set()

c.Authenticator.admin_users = {'zmcadmin'}

c.NativeAuthenticator.open_signup = True
c.Authenticator.allow_all = True
c.Spawner.start_timeout = 120 





