def install_software
  <<-SHELL
    apt-get update
    sudo apt install python3-pip ffmpeg python3-tk
  SHELL
end


Vagrant.configure("2") do |config|
  config.vm.box = "peru/ubuntu-18.04-desktop-amd64"
  config.vm.network "forwarded_port", guest: 5005, host: 5006
  config.vm.synced_folder ".", "/screeby", type: "rsync", rsync__exclude: ['.git/', '.idea/', 'venv/'], rsync__auto: true
  config.vm.provision "install_software", type: "shell", inline: install_software, run: 'never'
  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--audio", "none"]
  end
end
