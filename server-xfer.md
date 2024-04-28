# Transfer from Old Server to New

## SSH Alias

~/.ssh/config

```none
Host myflix
    HostName HOST
    User USER
    Port PORT
    IdentityFile /home/USER/.ssh/PRIVATESSH
```

## Transfer crossseed config

```bash
screen -dmS rsync_config sudo rsync -avz --update --progress --rsync-path="sudo rsync" myflix:/data/media/.config/cross-seed/ /.config/cross-seed/
```

## Transfer PostgreSQL 

```bash
screen -dmS rsync_pg sudo rsync -avz --update --progress --rsync-path="sudo rsync" myflix:/var/lib/postgresql/ /var/lib/postgresql/
```

## Transfer Plex Data

```bash
screen -dmS rsync_plex sudo rsync -avz --progress --delete-delay  --rsync-path="sudo rsync" myflix:/var/lib/plexmediaserver/ /.config/plexmediaserver/
```

## Transfer Bazarr Data

```bash
screen -dmS rsync_bazarr sudo rsync -avz --progress --update --rsync-path="sudo rsync" myflix:/opt/bazarr/ /.config/bazarrOpt/
```

## Transfer Media Data

```bash
screen -dmS rsync_library sudo rsync -ahHvP --partial-dir=.rsync-partial --bwlimit=50000 --include='media/***' --include='torrents/***' --exclude='*' --exclude='torrents/.RecycleBin/**' --exclude='torrents/orphaned_data/**' --exclude='media/.trash/**' --chown=bakerboy448:media --chmod=ug=rwX,o=rX --update -e ssh myflix:/data/media/ /mnt/data/ --log-file=/var/log/rsync_sx63_lib.log
```

## Transfer Torrent Data

```bash
screen -dmS rsync_library sudo rsync -ahHvP --partial-dir=.rsync-partial --bwlimit=1000000 --include='torrents/***' --exclude='*' --exclude='torrents/.RecycleBin/**' --exclude='torrents/orphaned_data/**' --exclude='media/.trash/**' --chown=bakerboy448:media --chmod=ug=rwX,o=rX --update -e ssh myflix:/data/media/ /mnt/data/ --log-file=/var/log/rsync_sx63.log
```

## Transfer Live Qbit

```bash
rsync -avz --update --chown=bakerboy448:bakerboy448 --chmod=ug=rwX,o=rX --progress myflix://home/bakerboy448/.local/share/qBittorrent/ /home/bakerboy448/.local/share/qBittorrent/
```

## Transfer Development

```bash
screen -dmS rsync_config sudo rsync -avz --update --progress --rsync-path="sudo rsync" myflix:/home/bakerboy448/_development /mnt/raid/
```
