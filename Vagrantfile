# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
  config.vm.box = "debian-60"
  # Port forwarding for Django's developemtn server.
  config.vm.forward_port 8000, 8000
  config.vm.provision :puppet
end
