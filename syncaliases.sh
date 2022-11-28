#!/bash
repo="https://raw.githubusercontent.com/bakerboy448/Scripts/"
branch="master"
if [ -n "${1+x}" ]; then
    user="$1"
else
    user="$USER"
fi
home=$(eval echo "~$user")

# Get the latest version of the sysrestart
sysrestart_path="/usr/bin/sysrestart"
sysrestart_name="sysrestart"
echo "Downloading latest version of the $sysrestart_path... using $repo/$branch/$sysrestart_name"
sudo wget -r --progress=bar -O "$sysrestart_path" "'$repo/$branch/$sysrestart_name'"
sudo chmod ug=rwx,o=rx "$sysrestart_path"
sudo chown root:root "$sysrestart_path"
sysrestart_ls=$("eval sudo ls -l $sysrestart_path")
echo "Updated $sysrestart_name at $sysrestart_path"
echo ""
echo "$sysrestart_ls"

# Get latest bashrc for current user
bashrc_path="$home/.bashrc"
bashrc_name=".bashrc"
echo "Downloading latest version of the $bashrc_path... using $repo/$branch/$bashrc_name"
sudo wget -r --progress=bar -O "$bashrc_path" "'$repo/$branch/$bashrc_name'"
sudo chmod 600 "$bashrc_path"
sudo chown "$user:$user" "$bashrc_path"
bashrc_ls=$("eval sudo ls -l $bashrc_path")
echo "Updated $bashrc_name for $user at $bashrc_path"
echo ""
echo "$bashrc_ls"

# Get latest bash aliases for current user
bashalias_path="$home/.bash_aliases"
bashalias_name=".bash_aliases"
echo "Downloading latest version of the $bashalias_path... using $repo/$branch/$bashalias_name"
sudo wget -r --progress=bar -O "$bashalias_path" "'$repo/$branch/$bashalias_name'"
sudo chmod 600 "$bashalias_path"
sudo chown "$user:$user" "$bashalias_path"
bashalias_ls=$("eval sudo ls -l $bashalias_path")
echo "Updated $bashalias_name for $user at $bashalias_path"
echo ""
echo "$bashalias_ls"

# Get latest bash functions for current user
bashfunctions_path="$home/.bash_functions"
bashfunctions_name=".bash_functions"
echo "Downloading latest version of the $bashfunctions_path... using $repo/$branch/$bashfunctions_name"
sudo wget -r --progress=bar -O "$bashfunctions_path" "'$repo/$branch/$bashfunctions_name'"
sudo chmod 600 "$bashfunctions_path"
sudo chown "$user:$user" "$bashfunctions_path"
bashfunctions_ls=$("eval sudo ls -l $bashfunctions_path")
echo "Updated $bashfunctions_name for $user at $bashfunctions_path"
echo ""
echo "$bashfunctions_ls"

# Add unattended-upgrades fix
fuck_unattended="01-fuck-unattended-upgrades.conf"
fuck_unattended_path="/etc/apt/apt.conf.d/$fuck_unattended"
echo "Downloading latest version of the $fuck_unattended_path... using $repo/$branch/$fuck_unattended"
sudo wget -r --progress=bar -O "$bashalias_path" "'$repo/$branch/$fuck_unattended'"
sudo chmod 644 "$fuck_unattended_path"
sudo chown root:root "$fuck_unattended_path"
fuck_unattended_path_ls=$("eval sudo ls -l $fuck_unattended_path")
echo "Updated $fuck_unattended for $user at $fuck_unattended_path"
echo ""
echo "$fuck_unattended_path_ls"
