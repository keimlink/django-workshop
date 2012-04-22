group { 'puppet':
    ensure => present,
}

class basic_setup {
    exec { 'apt-get update':
        command => '/usr/bin/apt-get update'
    }

    package { 'vim':
        ensure => present,
    }

    package { 'tree':
        ensure => present,
    }

    package { 'sqlite3':
        ensure => present,
    }
}

include basic_setup
