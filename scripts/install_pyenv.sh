apt-get update
apt install -y python3
apt install -y python3-pip
apt install -y build-essential libssl-dev libffi-dev python-dev
apt install -y git
apt-get install -y --no-install-recommends make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

/usr/sbin/useradd -m -d /opt/fichariod fichariod
/usr/sbin/usermod -L fichariod


cd /opt/fichariod
su - fichariod -c "curl https://pyenv.run | bash" # comes from https://github.com/pyenv/pyenv-installer

su - fichariod -c "echo '\n export PYENV_ROOT=\"/opt/fichariod/.pyenv\"' >> /opt/fichariod/.profile"
su - fichariod -c "echo '\n export PATH=\"\$PYENV_ROOT/bin:\$PATH\"' >> /opt/fichariod/.profile"
su - fichariod -c "echo '\n eval \"\$(pyenv init --path)\"' >> /opt/fichariod/.profile"

su - fichariod -c "echo '\n eval \"\$(pyenv init -)\"' >> /opt/fichariod/.bashrc"
su - fichariod -c "echo '\n eval \"\$(pyenv virtualenv-init -)\"' >> /opt/fichariod/.bashrc"


su - fichariod -c "pyenv update"
su - fichariod -c "pyenv install -v 3.8.7"

su - fichariod -c "pip3 install --user virtualenv"

su - fichariod -c "pyenv local 3.8.7"
su - fichariod -c "python -V"
su - fichariod -c "python3 -V"