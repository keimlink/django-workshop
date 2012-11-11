# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
  config.vm.box = "debian-60"
  # Port forwarding for Django's development server.
  config.vm.forward_port 8000, 8000
  config.vm.provision :chef_solo do |chef|
    chef.cookbooks_path = "cookbooks"
    chef.json = {
      "mysql" => {
        "server_root_password" => "django",
        "server_repl_password" => "django",
        "server_debian_password" => "django"
      },
      "postgresql" => {
        "password" => {
          "postgres" => "django"
        }
      }
    }
    chef.add_recipe "apt"
    chef.add_recipe "vim"
    chef.add_recipe "tree"
    chef.add_recipe "sqlite"
    chef.add_recipe "mysql"
    chef.add_recipe "postgresql::server"
  end
end
