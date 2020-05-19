def install_software
  <<-SHELL
    apt-get update
    sudo apt install -y ffmpeg python3-pip python3-tk python3-pil python3-pil.imagetk
  SHELL
end


Vagrant.configure("2") do |config|
  config.vm.box = "peru/ubuntu-18.04-desktop-amd64"
  config.vm.box_version = "20200501.01"
  config.vm.network "public_network"
  config.ssh.host = "192.168.43.114"
  config.ssh.port = 22
  config.vm.synced_folder "/home/sinaru/projects/screeby", "/screeby", type: "rsync", rsync__exclude: ['.git/', '.idea/'], rsync__auto: true
  config.vm.provider "virtualbox" do |vb|
     # Display the VirtualBox GUI when booting the machine
     vb.gui = true

      # Customize the amount of memory on the VM:
      vb.memory = "4096"
      vb.customize ["modifyvm", :id, "--vram", "128"]
  end
  config.vm.provision "install_software", type: "shell", inline: install_software
end
