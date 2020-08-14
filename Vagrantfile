# Script for installation of pyenv
$pyenvInstall = <<-'SCRIPT'
  sudo apt-get update

  # Install pyenv dependencies

  sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
  libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
  xz-utils tk-dev libffi-dev liblzma-dev python-openssl git

  # Instally pyenv
  git clone https://github.com/pyenv/pyenv.git ~/.pyenv

  echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
  echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile

  echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.profile

  source ~/.profile

SCRIPT

#Setup of python installations in pyenv


$pyenvSetup = <<-'SCRIPT'

  pyenv install 3.8.5
  pyenv global 3.8.5

SCRIPT


Vagrant.configure("2") do |config| 
 config.vm.box = "hashicorp/bionic64"

 config.vm.provision "shell", privileged: false, inline: $pyenvInstall
 config.vm.provision "shell", privileged: false, inline: $pyenvSetup


end