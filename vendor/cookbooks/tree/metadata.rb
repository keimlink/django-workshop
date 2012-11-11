name "tree"
version "1.0.0"
description "tree list contents of directories in a tree-like format."
long_description IO.read(File.join(File.dirname(__FILE__), 'README.md'))
maintainer "Markus Zapke-Gründemann"
maintainer_email "markus@keimlink.de"
license "Apache 2.0"

%w{debian ubuntu}.each do |os|
  supports os
end
