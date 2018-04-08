#!/bin/bash
sudo rm ./db_backup.gz
sudo mysqldump -u root dataset | gzip -c > db_backup.gz
