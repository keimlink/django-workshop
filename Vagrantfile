# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "boxcutter/debian82"

  config.vm.provider "vmware_fusion" do |v, override|
    override.vm.synced_folder ".", "/vagrant", type: "nfs"
  end

  # Port forwarding for Django's development server.
  config.vm.network "forwarded_port", guest: 8000, host: 8000,
    auto_correct: true

  # Port forwarding for LiveReload server.
  config.vm.network "forwarded_port", guest: 35729, host: 35729

  # Port forwarding for Glances server.
  config.vm.network "forwarded_port", guest: 61208, host: 61208

  # Salt provisioning.
  config.vm.synced_folder "salt/roots/", "/srv/"
  config.vm.provision :salt do |salt|
    salt.masterless = true
    salt.minion_config = "salt/minion"
    salt.run_highstate = true
  end
end
