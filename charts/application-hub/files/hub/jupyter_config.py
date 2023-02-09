import os
import sys

from tornado.httpclient import AsyncHTTPClient

configuration_directory = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, configuration_directory)

from z2jh import (
    get_name,
    get_name_env
)



# Configure JupyterHub to use the curl backend for making HTTP requests,
# rather than the pure-python implementations. The default one starts
# being too slow to make a large number of requests to the proxy API
# at the rate required.
AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")

c.ConfigurableHTTPProxy.api_url = (
    f'http://{get_name("proxy-api")}:{get_name_env("proxy-api", "_SERVICE_PORT")}'
)
c.ConfigurableHTTPProxy.should_start = False

# Don't wait at all before redirecting a spawning user to the progress page
c.JupyterHub.tornado_settings = {
    "slow_spawn_timeout": 0,
}

#c.KubeSpawner.image_pull_secrets =

jupyterhub_env = os.environ["JUPYTERHUB_ENV"].upper()
jupyterhub_hub_pod_namespace = os.environ["POD_NAMESPACE"].split(" ")[0]
jupyterhub_single_user_image = os.environ["JUPYTERHUB_SINGLE_USER_IMAGE"]
jupyterhub_auth_method = os.environ.get("JUPYTERHUB_AUTH_METHOD", "pam")
jupyterhub_oauth_callback_url = os.environ.get("JUPYTERHUB_OAUTH_CALLBACK_URL", "")
jupyterhub_oauth_client_id = os.environ.get("JUPYTERHUB_OAUTH_CLIENT_ID", "")
jupyterhub_oauth_client_secret = os.environ.get("JUPYTERHUB_OAUTH_CLIENT_SECRET", "")


jupyterhub_hub_host = f"hub.{jupyterhub_hub_pod_namespace}"
c.JupyterHub.authenticator_class = "jupyterhub.auth.DummyAuthenticator"
c.JupyterHub.cookie_secret_file = "/srv/jupyterhub/cookie_secret"
# Proxy config
c.JupyterHub.cleanup_servers = False
# Network
c.JupyterHub.allow_named_servers = False
c.JupyterHub.ip = "0.0.0.0"
c.JupyterHub.hub_ip = "0.0.0.0"
c.JupyterHub.hub_connect_ip = jupyterhub_hub_host
# Misc
c.JupyterHub.cleanup_servers = False

# Culling
c.JupyterHub.services = [
    {
        "name": "idle-culler",
        "admin": True,
        "command": [sys.executable, "-m", "jupyterhub_idle_culler", "--timeout=3600"],
    }
]

# Logs
c.JupyterHub.log_level = "DEBUG"

# Spawner
c.JupyterHub.spawner_class = "kubespawner.KubeSpawner"
c.KubeSpawner.environment = {
    "JUPYTER_ENABLE_LAB": "true",
}

c.KubeSpawner.uid = 1001
c.KubeSpawner.fs_gid = 100
c.KubeSpawner.hub_connect_ip = jupyterhub_hub_host

# SecurityContext
c.KubeSpawner.privileged = True

# ServiceAccount
c.KubeSpawner.service_account = "default"
c.KubeSpawner.start_timeout = 60 * 5
c.KubeSpawner.image = jupyterhub_single_user_image
c.KubernetesSpawner.verify_ssl = True
c.KubeSpawner.pod_name_template = (
    "jupyter-{username}-" + os.environ["JUPYTERHUB_ENV"].lower()
)

# NodeSelector
#c.KubeSpawner.node_selector = {"jupyter": "prod"}

# Namespace
c.KubeSpawner.namespace = jupyterhub_hub_pod_namespace

# User namespace
c.KubeSpawner.enable_user_namespaces = True

# Volumes
c.KubeSpawner.storage_capacity = "10Gi"
c.KubeSpawner.storage_class = "managed-nfs-storage"
c.KubeSpawner.storage_pvc_ensure = True
c.KubeSpawner.pvc_name_template = (
    "claim-{username}-" + os.environ["JUPYTERHUB_ENV"].lower()
)
c.KubeSpawner.volumes = [
    {
        "name": "volume-workspace-{username}-" + os.environ["JUPYTERHUB_ENV"].lower(),
        "persistentVolumeClaim": {
            "claimName": "claim-{username}-" + os.environ["JUPYTERHUB_ENV"].lower()
        },
    },
]
c.KubeSpawner.volume_mounts = [
    {
        "name": "volume-workspace-{username}-" + os.environ["JUPYTERHUB_ENV"].lower(),
        "mountPath": "/workspace",
    }
]