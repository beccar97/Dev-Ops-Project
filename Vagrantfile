Vagrant.configure("2") do |config| 
 config.vm.box = "hashicorp/bionic64"

 config.vm.provision "shell", inline: <<-SHELL
  sudo apt-get update

  # TODO: Install pyenv prerequisites
  # TODO: Install pyenv
SHELL


end