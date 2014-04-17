git-bump and git-deploy
=======================

An extension for git that allows for sane and pain-free code deployments, by utilising tags.

Usage
-----

1. All the scripts (git-deploy, git-bump, and the respective helpers) go somewhere in your `$PATH`
    * The easiest way to do this is probably to add this repo to your `$PATH`
2. The manpages go in your manpath
    * You could make a couple of symlinks to them from `~/.local/share/man/man1/` if your distro rolls that way.
3. Deployment config goes in the root of your repo, in `.git-deploy`
4. Bump the version number with `git bump <environment>`
4. Deploy that tag with `git deploy <environment>`


Config example
--------------

```
[environment "staging"]
	versioning = ANCHOR-STANDARD-STAGING
	user = deploy
	host = stg.example.com
	command = cd /home/umad/app/ && git fetch --tags && git checkout %s && sudo /usr/local/bin/allah restart umad

[environment "production"]
	versioning = ANCHOR-STANDARD-PRODUCTION
	user = deploy
	host = prod1.example.com,prod2.example.com,prod3.example.com
	command = cd /home/umad/app/ && git fetch --tags && git checkout %s && sudo /usr/local/bin/allah restart umad

# vim: syntax=gitconfig
```
