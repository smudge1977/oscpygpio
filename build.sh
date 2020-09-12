sudo chown -R root:root project-1.0/

sudo cp ./project-1.0/src/project/project ./project-1.0/usr/bin/project

find ./project-1.0/DEBIAN -type d | xargs chmod 755

sudo chmod 0775 ./project-1.0/DEBIAN/control

sudo dpkg-deb --build ./project-1.0/

dpkg -i ./project-1.0.deb






