Use git config files - it's there, might as well use them!

Git process is `git fetch` then `git checkout $TAG`. This guards against weirdness on the deployment target, like being checked out to some other branch, etc. git pull is *definitely* wrong, as that performs a merge.

Namespace the config sections, eg. `[environment.staging]`

Names like "staging" are NOT special except to humans.

Define as much behaviour as possible in the config, not in the code. That said, do write functionality in the code, then expose it for selection by the user as a "token" (eg. the anchor-standard-staging versioning style)

`git config -f dot-git-deploy environment.staging.versioning anchor-standard-staging`

```
[environment.dev]
	versioning = DATED
	user = deploy
	host = dev.example.com

[environment.staging]
	versioning = ANCHOR-STANDARD-STAGING
	user = deploy
	host = stg.example.com

[environment.production]
	versioning = ANCHOR-STANDARD-PRODUCTION
	user = deploy
	host = example.com
```

Two separate features:

* bump
* deploy

**Bump** performs the functions of calculating the next version number, and adding the tag. It then emits the tag to stdout.

**Deploy** is completely independent of bump, and simply arranges for the specified environment to be deployed to.


BUMP
====

Bump's logic
------------

1. Decide WHAT to tag
2. Is it SAFE to tag?
3. WHAT is the new tag?
4. APPLY the tag
5. EMIT the tag to stdout

The first three steps implement **policy** as codified in a version-bumper-helper (eg. ANCHOR-STANDARD-STAGING).
The fourth step applies the tag to the repo.
The fifth and last step echos the new tag, which can either be used by a human, or another tool like git-deploy.


Example usage
-------------

```
git bump staging
git bump production
git bump yourmum
```

Versioning logic
----------------

Anchor Standard Staging:

* WHAT? Do we assume we're tagging `HEAD` of `master`?
* Check that you're on `master`
* Check that you're up to date
*     vX.Y    => vX.(Y+1)
*     vX.YrcR => vX.Yrc(R+1)

Anchor Standard Production:

* Find the "last" rc (staging) tag
* Do you have any rc tags? Do you have to have one first?
*     vX.YrcR => vX.Y

