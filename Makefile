# My hands are used to type make for everything ...

help:
	@echo
	@echo "Options are:"
	@echo
	@echo "  - create-db :   DROPS and creates database"
	@echo "  - runspider :   runs the spider"
	@echo "  - dump-db   :   dumps the database"
	@echo
	@echo "(you need to export the root password ROOTPWD)"
	@echo

create-db:
	-mysql -u root -p$(ROOTPWD) -e "DROP DATABASE quoky;"
	mysql -u root -p$(ROOTPWD) -e "CREATE DATABASE quoky;"
	mysql -u root -p$(ROOTPWD) -e "GRANT USAGE on *.* to 'quoky'@'localhost' IDENTIFIED BY 'mypass';"
	mysql -u root -p$(ROOTPWD) -e "GRANT ALL PRIVILEGES ON quoky.* to 'quoky'@'localhost';"

runspider:
	scrapy runspider quoky/spiders/quoka.py

dump-db:
	mysqldump -u quoky -pmypass quoky > dumps/quoky.dump
