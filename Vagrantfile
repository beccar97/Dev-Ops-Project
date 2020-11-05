$pyenvInstall = <<-'SCRIPT'
  sudo apt-get update

  # Install pyenv dependencies

  sudo apt-get install -y -q build-essential libssl-dev zlib1g-dev libbz2-dev \
  libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
  xz-utils tk-dev libffi-dev liblzma-dev python-openssl git

  # Install pyenv
  git clone https://github.com/pyenv/pyenv.git ~/.pyenv

  echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
  echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile

  echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.profile
  
SCRIPT

$pyenvSetup = <<-'SCRIPT'

  pyenv install 3.8.5
  pyenv global 3.8.5
SCRIPT


$seleniumInstall = <<-'SCRIPT'
  curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb
  apt-get install ./chrome.deb -y -q
  sudo mv chrome /usr/local/bin
  rm ./chrome.deb

  curl -sSL https://chromedriver.storage.googleapis.com/${LATEST}/chromedriver_linux64.zip -o chromedriver_linux64.zip &&\
  apt-get install unzip -y -q
  unzip ./chromedriver_linux64.zip
  sudo mv chromedriver /usr/local/bin/
  rm -r chromedriver*

SCRIPT

$poetryInstall = <<-'SCRIPT'
   curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
SCRIPT

$runProject = <<-'SCRIPT'
  cd "/vagrant"
  poetry install
  nohup poetry run flask run --host 0.0.0.0 > logfile 2>&1 &
SCRIPT

Vagrant.configure("2") do |config| 
  config.vm.box = "hashicorp/bionic64"

  config.vm.provision "shell", privileged: false, inline: $pyenvInstall
  config.vm.provision "shell", privileged: false, inline: $pyenvSetup
  config.vm.provision "shell", privileged: false, inline: $seleniumInstall
  config.vm.provision "shell", privileged: false, inline: $poetryInstall

  config.vm.network "forwarded_port", guest: 5000, host: 5000

  config.trigger.after :up do |trigger|
    trigger.name = "Launch app"
    trigger.info = "Running TODO app setup script"
    trigger.run_remote = {privileged: false, inline: $runProject }
  end
end
