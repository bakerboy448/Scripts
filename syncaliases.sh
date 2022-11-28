#!/bash
repo="https://raw.githubusercontent.com/bakerboy448/Scripts/"
branch="master"

# Get the latest version of the sysrestart
sysrestart_path="/usr/bin/sysrestart"
sysrestart_name="sysrestart"
echo "Downloading latest version of the $sysrestart_name..."
sudo curl -o "$sysrestart_path" "$repo/$branch/$sysrestart_name"
sudo chmod ug=rwx,o=rx "$sysrestart_path"
sudo chown root:root "$sysrestart_path"
sysrestart_ls=$("ls -l $sysrestart_path")
echo "Updated $sysrestart_name"
echo ""
echo "$sysrestart_ls"

# Get latest bashrc for current user
bashrc_path="$HOME/.bashrc"
bashrc_name=".bashrc"
echo "Downloading latest version of the $bashrc_name..."
curl -o "$bashrc_path" "$repo/$branch/$bashrc_name"
sudo chmod 600 "$bashrc_path"
sudo chown "$USER:$USER" "$bashrc_path"
bashrc_ls=$("ls -l $bashrc_path")
echo "Updated $bashrc_name for $USER"
echo ""
echo "$bashrc_ls"

# Get latest bash aliases for current user
bashalias_path="$HOME/.bash_aliases"
bashalias_name=".bash_aliases"
echo "Downloading latest version of the $bashalias_name..."
curl -o "$bashalias_path" "$repo/$branch/$bashalias_name"
sudo chmod 600 "$bashalias_path"
sudo chown "$USER:$USER" "$bashalias_path"
bashalias_ls=$("ls -l $bashalias_path")
echo "Updated $bashalias_name for $USER"
echo ""
echo "$bashalias_ls"

# Get latest bash functions for current user
bashfunctions_path="$HOME/.bash_functions"
bashfunctions_name=".bash_functions"
echo "Downloading latest version of the $bashfunctions_name..."
curl -o "$bashfunctions_path" "$repo/$branch/$bashfunctions_name"
sudo chmod 600 "$bashfunctions_path"
sudo chown "$USER:$USER" "$bashfunctions_path"
bashfunctions_ls=$("ls -l $bashfunctions_path")
echo "Updated $bashfunctions_name for $USER"
echo ""
echo "$bashfunctions_ls"

# Add unattended-upgrades fix
fuck_unattended="01-fuck-unattended-upgrades.conf"
fuck_unattended_path="/etc/apt/apt.conf.d/$fuck_unattended"
echo "Downloading latest version of the $fuck_unattended..."
sudo curl -o "$bashalias_path" "$repo/$branch/$fuck_unattended"
sudo chmod 644 "$fuck_unattended_path"
sudo chown root:root "$fuck_unattended_path"
fuck_unattended_path_ls=$("ls -l $fuck_unattended_path")
echo "Updated $fuck_unattended for $USER"
echo ""
echo "$fuck_unattended_path_ls"
source $HOME/.bashrc
