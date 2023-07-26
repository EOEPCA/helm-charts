import glob
import os
import re
import sys

from binascii import a2b_hex

from tornado.httpclient import AsyncHTTPClient
from jupyterhub.utils import url_path_join
from oauthenticator.generic import GenericOAuthenticator


from traitlets import Unicode
from tornado.httputil import url_concat
from tornado.httpclient import HTTPRequest



from application_hub_context.app_hub_context import DefaultApplicationHubContext


config_path="/usr/local/etc/applicationhub/config.yml"
configuration_directory = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, configuration_directory)

from z2jh import (
    get_config,
    set_config_if_not_none,
    get_name,
    get_name_env,
    get_secret_value,
)



def custom_options_form(spawner):

    spawner.log.info("Configure profile list")


    namespace = f"{resource_manager_workspace_prefix}-{spawner.user.name}"
    workspace = DefaultApplicationHubContext(
        namespace=namespace,
        spawner=spawner,
        config_path=config_path
    )

    spawner.profile_list = workspace.get_profile_list()

    return spawner._options_form_default()


def pre_spawn_hook(spawner):

    profile_slug = spawner.user_options.get("profile", None)

    env = os.environ["JUPYTERHUB_ENV"].lower()
    
    spawner.environment["CALRISSIAN_POD_NAME"] = f"jupyter-{spawner.user.name}-{env}"

    spawner.log.info(f"Using profile slug {profile_slug}")

    #namespace = f"jupyter-{spawner.user.name}"
    namespace = f"{resource_manager_workspace_prefix}-{spawner.user.name}"

    workspace = DefaultApplicationHubContext(
        namespace=namespace,
        spawner=spawner,
        config_path=config_path
    )

    workspace.initialise()

    spawner.log.info(f"env: {spawner.environment.get('JPY_DEFAULT_URL')}")

def post_stop_hook(spawner):

    #namespace = f"jupyter-{spawner.user.name}"
    namespace = f"{resource_manager_workspace_prefix}-{spawner.user.name}"

    workspace = DefaultApplicationHubContext(
        namespace=namespace,
        spawner=spawner,
        config_path=config_path
    )
    spawner.log.info("Dispose in post stop hook")
    workspace.dispose()


# Configure JupyterHub to use the curl backend for making HTTP requests,
# rather than the pure-python implementations. The default one starts
# being too slow to make a large number of requests to the proxy API
# at the rate required.
AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")

c.ConfigurableHTTPProxy.api_url = (
    f'http://{get_name("proxy-api")}:{get_name_env("proxy-api", "_SERVICE_PORT")}'
)

print(f"c.ConfigurableHTTPProxy.api_url = {c.ConfigurableHTTPProxy.api_url}")
c.ConfigurableHTTPProxy.should_start = False

# Don't wait at all before redirecting a spawning user to the progress page
c.JupyterHub.tornado_settings = {
    "slow_spawn_timeout": 0,
}

class EoepcaOAuthenticator(GenericOAuthenticator):
    login_service = Unicode("EOEPCA", config=True)
    id_token = None
    print("LOGIN EOEPCA")


    def _get_user_data(self, token_response):
        access_token = token_response['access_token']
        token_type = token_response['token_type'].capitalize()

        # Determine who the logged in user is
        headers = {
            "Accept": "application/json",
            "User-Agent": "JupyterHub",
            "Authorization": "{} {}".format(token_type, access_token)
        }
        if self.userdata_url:
            url = url_concat(self.userdata_url, self.userdata_params)
        else:
            raise ValueError("Please set the OAUTH2_USERDATA_URL environment variable")

        if self.userdata_token_method == "url":
            url = url_concat(self.userdata_url, dict(access_token=access_token))

        req = HTTPRequest(url, headers=headers)
        return self.fetch(req, "fetching user data")

    @staticmethod
    def _create_auth_state(token_response, user_data_response):
        access_token = token_response['access_token']
        refresh_token = token_response.get('refresh_token', None)
        scope = token_response.get('scope', '')
        id_token = token_response['id_token']
        if isinstance(scope, str):
            scope = scope.split(' ')

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'oauth_user': user_data_response,
            'scope': scope,
            'id_token': id_token
        }
    
    async def pre_spawn_start(self, user, spawner):
        """Pass upstream_token to spawner via environment variable"""
        auth_state = await user.get_auth_state()
        if not auth_state:
            # auth_state not enabled
            return
        spawner.environment['ID_TOKEN'] = auth_state['id_token']



jupyterhub_env = os.environ["JUPYTERHUB_ENV"].upper()
jupyterhub_hub_host = "application-hub-hub.proc"
jupyterhub_single_user_image = os.environ["JUPYTERHUB_SINGLE_USER_IMAGE_NOTEBOOKS"]

resource_manager_workspace_prefix = os.environ["RESOURCE_MANAGER_WORKSPACE_PREFIX"]


c.JupyterHub.authenticator_class = EoepcaOAuthenticator
c.Authenticator.enable_auth_state = True
c.Authenticator.admin_users = {'eric','bob'} 

c.Authenticator.scope = 'openid email user_name is_operator'.split(' ')

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
c.KubeSpawner.allow_privilege_escalation = True

# ServiceAccount
c.KubeSpawner.service_account = "default"
c.KubeSpawner.start_timeout = 60 * 10
c.KubeSpawner.image = jupyterhub_single_user_image
c.KubernetesSpawner.verify_ssl = True
c.KubeSpawner.pod_name_template = (
    "jupyter-{username}-" + os.environ["JUPYTERHUB_ENV"].lower()
)

# NodeSelector
c.KubeSpawner.node_selector = {"node-role.kubernetes.io/worker": "true"}

# Namespace
c.KubeSpawner.namespace = "proc"

# User namespace
c.KubeSpawner.enable_user_namespaces = True
c.KubeSpawner.user_namespace_template = (
    resource_manager_workspace_prefix + "-{username}"
)

c.KubeSpawner.options_form = custom_options_form
#c.KubeSpawner.image_pull_policy = "IfNotPresent"
c.KubeSpawner.image_pull_policy = "Always"

# hooks
c.KubeSpawner.pre_spawn_hook = pre_spawn_hook
c.KubeSpawner.post_stop_hook = post_stop_hook
