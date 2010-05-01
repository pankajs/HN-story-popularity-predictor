from fabric.api import local


def devel_virtualenv():
    """Set up a local devel virtualenv."""
    local('easy_install -U setuptools')
    local('easy_install pip')
    local('pip install -r dev-requirements.txt')
