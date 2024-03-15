# Silly Software

**Author: [`Malcolm Seyd`](https://github.com/malcolmseyd)**

**Category: `Cloud Easy`**

## Description

We're Silly Software, and we like bringing the Fun back into devops! We've decided that we're going to start distributing our software as Docker images, because that seems like the most fun! I hope nothing goes wrong :)

```
docker run public.ecr.aws/d8p5p1v7/vikectf2024/silly-software:latest
```

## Organizers

Build the docker image using the Dockerfile in `src/silly-software` and upload it to a registry. Users should get a container registry and the name of the Docker image, they are expected to download the image themselves.

I used a free trial of https://fury.co to host the private container registry, but you can do so however you'd like. I liked that I could provide read-only auth keys and it was easy to upload packages one-off.

## Solution

According to [the spec](https://github.com/moby/docker-image-spec/blob/617aa3ab78e1c633e9a09397b279c6eb856aed22/spec.md), Docker images are just a tarball of tarballs. We can dump this tarball to the filesystem like so:

```console
$ docker save -o ball.tar silly-software
$ tar -xf ball.tar
$ ls
ball.tar  blobs/  index.json  manifest.json  oci-layout  repositories
```

If we check out `manifest.json`, it keeps a list of every layer. The order of the layers correspond with the history of the tarball. Let's check out the history:

```console
$ docker history silly-software
IMAGE          CREATED          CREATED BY                                      SIZE      COMMENT
8cc53b07aa4b   2 minutes ago    CMD ["npm" "run" "start"]                       0B        buildkit.dockerfile.v0
<missing>      2 minutes ago    RUN /bin/sh -c rm .npmrc # buildkit             0B        buildkit.dockerfile.v0
<missing>      22 minutes ago   RUN /bin/sh -c npm install --omit=dev # buil…   2.22MB    buildkit.dockerfile.v0
<missing>      22 minutes ago   COPY index.js package.json package-lock.json…   1.39kB    buildkit.dockerfile.v0
... blah blah blah ...
```

The top few layers look interesting. Let's untar whatever we can:

```console
$ for f in *; do tar -xf "$f"; done
tar: This does not look like a tar archive
tar: Exiting with failure status due to previous errors
tar: This does not look like a tar archive
tar: Exiting with failure status due to previous errors
tar: This does not look like a tar archive
...
$ ls
09203fe24ebe3b9bf3b423804f67c094ff29d1cc576f90a90de38f59988b07b3
135d52801503d22440917b88074a3b807b9afba2fea219268b8b7201bbd874be
16e3df8e819473fac834f7877610d2fc379550686d2a3bc2a9a7dd328a0a5f21
1a5fc1184c481caeb279bce728e080daba423b5215282318ba86e9b8c388a2b4
1c4fd74565106f27e277b6a7ee88670f7a75eb114dac1548341bfad3e405b7f8
... blah blah ...
app
bb13f20ca0b7e6e3596caafcaeed25d7c3519bc7f8089ccf4ebc73c8927ea2eb
bin
boot
c963957a122761d05606b39c0973f8c78f05e63fe98294446b875dd7fc408cdf
dev
etc
f3f47b3309ca3efcca62cc16aee76177047f0535d9ea6a03546be0b8bee30ded
home
lib
lib64
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
```

Let's explore `/app`. It's a JavaScript app that has two dependencies. It looks like the only dev dependency is the flag, so let's install it! This is only possible because we have a special auth token in `/app/.npmrc`, which `npm` will use if we're in the folder.

```console
$ npm i

added 1 package, and audited 3 packages in 363ms

found 0 vulnerabilities
$ cd node_modules/the-flag/
$ ls
index.js  package.json  the-flag-1.0.0.tgz
$ cat index.js 
export const flag = "vikeCTF{p33L_1t_L1k3_4N_0n1oN}"
```
