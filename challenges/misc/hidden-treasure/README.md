# Hidden Treasure

**Author: [`Kyle Stang`](https://github.com/kylestang)**

**Category: `Misc Medium`**

## Organizers

Participants should be given vikebox.img.gz, an image of an ubuntu VM, and told they
need to gain access to `http://35.94.129.106:3005/`. They should also be told
the user may have the credentials to the site.
They will then have to search the filesystem and gain access.

The website should be hosted by running `docker compose up`.

## Solution

After extracting `vikebox.img`, we can use the `file` command to confirm
it's a disk image.
```console
❯ file vikebox.img
vikebox.img: DOS/MBR boot sector, extended partition table (last)
```
Let's inspect the disk to see what partitions are on it:
```console
❯ fdisk -l vikebox.img
Disk vikebox.img: 15 GiB, 16106127360 bytes, 31457280 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: 1B23F900-9049-4FA9-A7AC-B8A548AB08A3

Device         Start      End  Sectors  Size Type
vikebox.img1    2048     4095     2048    1M BIOS boot
vikebox.img2    4096  1054719  1050624  513M EFI System
vikebox.img3 1054720 31455231 30400512 14.5G Linux filesystem
```

Partition 3, the Linux filesystem, seems the most interesting.
We can then create a loopback device for partition 3 and mount it like so:
```console
❯ sudo losetup -Pf vikebox.img --show
/dev/loop0

❯ sudo mount /dev/loop0p3 /mnt/loop0p3/
```

Opening the app we have a standard Ubuntu filesystem.
Since we know we need to gain access to a website that the user has accessed
before, we should probably take a look at the web browser.

The firefox cookies file is stored in
`/home/viktor/snap/firefox/common/.mozilla/firefox/gafhcvjb.default/cookies.sqlite`.

Opening it with sqlite3, we can search for cookies that match our site:
```sql
sqlite> SELECT * FROM moz_cookies WHERE host LIKE '35.94.129.106';
317||session|6090a4914358dc1fce139aa4e11df13009c2eda2b75d35d537706d7313237389|35.94.129.106|/|1709885275|1709798941703576|1709798880154955|0|0|0|0|0|1
```

Looks like we have a session cookie!
Stealing the cookie and adding it to our own request, the site gives us the flag.

## Flag
```
vikeCTF{sh0rtbr3@d_c1nn@m0n_br0w53r}
```
