# My Buddy Erik

**Author: [`Malcolm Seyd`](https://github.com/malcolmseyd)**

**Category: `Cloud Easy`**

## Description

My buddy Erik wants to play Minecraft so I set up a server for us to play on. I've commited my configuration to GitHub because it's so convenient! Can you make sure that everything is secure?

## Organizers

Make sure to start with an **empty GitHub repo**. Pass an SSH remote URL into the setup script and let the magic happen:

```console
$ ./setup.sh "git@github.com:OWNER/REPO.git"
```

The flag is hardcoded into the Git tarball, so don't leak it!

If you're testing the solution on a private repo, be sure to include then Authorization header. See the linked API docs for more info.

## Solution

The Git tarball contains two branches: `original` and `fixed`. Viktor Viking accidentally committed his RCON password and pushed to GitHub, so he had to rebase it out of history and force push to delete it. We left a hint by forcing the rebase to keep the revert commit for the RCON password.

GitHub retains all repo events for 90 days, and we can use [the API](https://docs.github.com/en/rest/activity/events?apiVersion=2022-11-28#list-repository-events) to access this event history. This history includes metadata about all commits pushed to the repo!

```console
$ curl "https://api.github.com/repos/OWNER/REPO/events"
[
  {
    "id": "36207240383",
    "type": "PushEvent",
... snip ...
        {
          "sha": "551a06d75f125b246a838b48dbe6a768f36b8708",
          "author": {
            "email": "viktor@vikesec.ca",
            "name": "Viktor Viking"
          },
          "message": "Add RCON password",
          "distinct": true,
          "url": "https://api.github.com/repos/OWNER/REPO/commits/551a06d75f125b246a838b48dbe6a768f36b8708"
        },
... more stuff ...
```

We've found the commit where Viktor added the RCON password. We can open a random commit in GitHub, take the SHA, and plug it right into the address bar. It should look something like this:

```
https://github.com/OWNER/REPO/commit/04946943e58780fa3ce9efcebbcd4e32e56e1958
```

Hit enter and voila, you should have the password! Surprisingly, GitHub retains commits with no branch, and they're publicly visible through this event log. If you push a secret to a public GitHub, ever, you need to rotate it immediately. Stay safe out there!
