sudo systemctl start postgresql.service
sudo -i -u postgres
psql
# use name of role is feeds   superuser yes
sudo -u postgres createuser --interactive
sudo -u postgres createdb feeds
sudo adduser feeds
sudo -u feeds psql
