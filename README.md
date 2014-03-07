git-deploy
==========

An extension for git that allows for sane and pain-free code deployments, by utilising tags

Usage
-----

1. `git-deploy` goes somewhere in your `$PATH`
2. `git-deploy.1` goes in your manpath
3. Deployment config goes in the root of your repo, in `.gitdeploy-ENV_NAME`
4. Deploy with `git deploy ENV_NAME`


Config example
--------------

```
export GITDEPLOY_SSH_HOST="production.example.com"
export GITDEPLOY_SSH_USER="appuser"
export GITDEPLOY_DIR="~/app"
export GITDEPLOY_MAKETARGET="pull_and_deploy"
```
