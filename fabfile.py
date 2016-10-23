from fabric.api import *
import fabric.contrib.project as project
import os

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output'
DEPLOY_PATH = env.deploy_path

# Remote server configuration
production = 'root@web1.elliottucker.net:22'
dest_path = '/var/www/html'



def clean():
    if os.path.isdir(DEPLOY_PATH):
        local('rm -rf {deploy_path}'.format(**env))
        local('mkdir {deploy_path}'.format(**env))

def build():
    local('pelican -s pelicanconf.py')

def rebuild():
    clean()
    build()

def regenerate():
    local('pelican -r -s pelicanconf.py')

def serve():
    local('cd {deploy_path} && python -m SimpleHTTPServer'.format(**env))

def reserve():
    build()
    serve()

def preview():
    local('pelican -s publishconf.py')

def cf_upload():
    rebuild()
    local('cd {deploy_path} && '
          'swift -v -A https://auth.api.rackspacecloud.com/v1.0 '
          '-U {cloudfiles_username} '
          '-K {cloudfiles_api_key} '
          'upload -c {cloudfiles_container} .'.format(**env))


@hosts(production)
def setupserver():
  sudo("systemctl stop nginx")
  sudo("letsencrypt certonly --standalone --non-interactive  --agree-tos --email elliot.tucker@gmail.com -d elliottucker.net -d www.elliottucker.net -d mail.elliottucker.net")
  sudo('echo "01 01 * * * root letsencrypt renew --webroot -w /var/www/html" >> /etc/crontab')
  with cd("/etc/nginx/sites-enabled"):
    put("nginx_default", "default")
  put("keybase.txt", "{}/.well-known/keybase.txt".format(dest_path))
  sudo("systemctl restart nginx")


@hosts(production)
def publish():
    local('pelican -s publishconf.py')
    project.rsync_project(
        remote_dir=dest_path,
        exclude=[".DS_Store","photos"],
        local_dir=DEPLOY_PATH.rstrip('/') + '/',
        delete=True
    )
