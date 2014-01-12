# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "debian72"

  config.vm.box_url = "https://bitbucket.org/keimlink/django-workshop/downloads/debian72.box"
  config.vm.box_download_checksum_type = "sha256"
  config.vm.box_download_checksum = "28890f1f0a6409d8f6988b9a9a292ed777f1aa3a9b195e453643eb6204472e4b"
  config.vm.provider "vmware_fusion" do |v, override|
    override.vm.box_url = "https://bitbucket.org/keimlink/django-workshop/downloads/debian72_vmware.box"
    override.vm.box_download_checksum = "e721719458feec14a34514d87296f573813e2a3889735ae0fc4d3e770c8e55ab"
    override.vm.synced_folder ".", "/vagrant", type: "nfs"
  end

  # Port forwarding for Django's development server.
  config.vm.network "forwarded_port", guest: 8000, host: 8000,
    auto_correct: true

  # Salt provisioning.
  config.vm.synced_folder "salt/roots/", "/srv/"
  config.vm.provision :salt do |salt|
    salt.minion_config = "salt/minion"
    salt.run_highstate = true
  end
end
