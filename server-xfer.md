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
## 2025-04 Transfer

## run as sudo
```bash
sudo -i
```
# Move Config
```bash
screen -dmS rsync_data_config sudo RSYNC_RSH="ssh -o Compression=no" rsync -aAXHv --delete-after --info=progress2,stats,flist,name,del,skip --bwlimit=85000 --stats --rsync-path="sudo rsync" --exclude=*.log --log-file=/var/log/rsync/rsync_data_config.log myflix:/.config/ /.config/
```
# Move DL
```bash
screen -dmS rsync_data_torrents sudo RSYNC_RSH="ssh -o Compression=no" rsync -aAXHvW --delete-after --info=progress2,stats,flist,name,del,skip --bwlimit=95000 --stats --rsync-path="sudo rsync" --exclude=*.trash --log-file=/var/log/rsync/rsync_data_torrents.log --link-dest=/mnt/data/torrents.new/ myflix:/mnt/data/torrents/ /mnt/data/torrents/
```

# Move Existing Data
```bash
screen -dmS rsync_data_data sudo RSYNC_RSH="ssh -o Compression=no" rsync -aAXHvW --delete-after --info=progress2,stats,flist,name,del,skip --bwlimit=95000 --stats --rsync-path="sudo rsync" --exclude=*.trash --exclude=link_source* --exclude=raid* --exclude=torrents.new* --log-file=/var/log/rsync/rsync_data_data.log --link-dest=/mnt/data/torrents.new/ myflix:/mnt/data/ /mnt/data/
```
# Move All Data
```bash
screen -dmS rsync_data_data sudo RSYNC_RSH="ssh -o Compression=no" rsync -aAXHv --delay-updates --delete-after --info=progress2 --bwlimit=45000 --stats --rsync-path="sudo rsync" --exclude=*.trash --exclude=raid/* --exclude=link_source/* --exclude=raid/* --exclude=torrents.new/* --exclude=file_list.txt --log-file=/var/log/rsync/rsync_data_data.log --link-dest=/mnt/zfs-data/torrents.new/ --temp-dir=/mnt/data/tmp --files-from=/mnt/data/file_list.txt myflix:/mnt/data/ /mnt/zfs-data/
```
# Move Qbit
```bash
screen -dmS rsync_data_qbt_share sudo RSYNC_RSH="ssh -o Compression=no" rsync -aAXHv --delay-updates --delete-after --info=progress2 --bwlimit=85000 --stats --rsync-path="sudo rsync" myflix:/home/bakerboy448/.local/share/qBittorrent/ /home/qbittorrent/.local/share/qBittorrent/
```
```bash
screen -dmS rsync_data_qbt_config sudo RSYNC_RSH="ssh -o Compression=no" rsync -aAXHv --delay-updates --delete-after --info=progress2 --bwlimit=85000 --stats --rsync-path="sudo rsync" myflix:/home/bakerboy448/.config/qBittorrent/ /home/qbittorrent/.config/qBittorrent/
```
# Fix Ownership
```bash
chown -R qbittorrent:media /home/qbittorrent/
```
