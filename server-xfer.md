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
screen -dmS rsync_library rsync -avz --update --chown=bakerboy448:media --chmod=ug=rwX,o=rX --progress myflix://data/media/media/ /mnt/data/media/
```

## Transfer Torrent Data

```bash
screen -dmS rsync_torrents rsync -avz --progress --update --exclude='.RecycleBin' --exclude='orphaned_data' --chown=bakerboy448:media --chmod=ug=rwX,o=rX -e ssh myflix:/data/media/torrents /mnt/data/
```

## Transfer Live Qbit

```bash
rsync -avz --update --chown=bakerboy448:bakerboy448 --chmod=ug=rwX,o=rX --progress myflix://home/bakerboy448/.local/share/qBittorrent/ /home/bakerboy448/.local/share/qBittorrent/
```

## Transfer Development

```bash
screen -dmS rsync_config sudo rsync -avz --update --progress --rsync-path="sudo rsync" myflix:/home/bakerboy448/_development /mnt/raid/
```
