#!/bin/bash

/usr/bin/mysqld_safe > /dev/null 2>&1 &

RET=1
while [[ RET -ne 0 ]]; do
    echo "=> Waiting for confirmation of MySQL service startup"
    sleep 5
    mysql -uroot -e "status" > /dev/null 2>&1
    RET=$?
done

PASS=${MYSQL_ADMIN_PASS:-$(pwgen -s 12 1)}
_word=$( [ ${MYSQL_ADMIN_PASS} ] && echo "preset" || echo "random" )
echo "=> Creating MySQL admin user with ${_word} password"

echo 1
mysql -uroot -e "CREATE USER 'admin'@'%' IDENTIFIED BY '$PASS'"
echo 2
mysql -uroot -e "GRANT ALL PRIVILEGES ON *.* TO 'admin'@'%' WITH GRANT OPTION"
echo 3
mysql -uroot -e " GRANT ALL PRIVILEGES ON phpmyadmin.* TO  'pma'@'localhost' IDENTIFIED BY ''"
echo 4


_user=${MYSQL_USER_NAME:-user}
_userdb=${MYSQL_USER_DB:-db}
_userpass=${MYSQL_USER_PASS:-password}

echo "=> Creating MySQL user in db ${_userdb} with username ${_user} and ${_userpass} password"

mysql -uroot -e "CREATE USER '${_user}'@'%' IDENTIFIED BY  '${_userpass}'"
mysql -uroot -e "GRANT USAGE ON *.* TO  '${_user}'@'%' IDENTIFIED BY '${_userpass}'"
mysql -uroot -e "CREATE DATABASE IF NOT EXISTS ${_userdb}"
mysql -uroot -e "GRANT ALL PRIVILEGES ON ${_userdb}.* TO '${_user}'@'%'"

mysql -uroot -D${_userdb} < /init_db.sql
mysql -uroot -D${_userdb} -e "INSERT INTO tbl_users_2 VALUES ('admin', md5('${EXPOLITABLE_ADMIN_PASS}'), '${RAW_FLAG}');"

echo "=> Done!"

echo "========================================================================"
echo "You can now connect to this MySQL Server with $PASS"
echo ""
echo "    mysql -uadmin -p$PASS -h<host> -P<port>"
echo ""
echo "Please remember to change the above password as soon as possible!"
echo "MySQL user 'root' has no password but only allows local connections"
echo ""

echo "We also created"
echo "A database called '${_userdb}' and"
echo "a user called '${_user}' with password '${_userpass}'"
echo "'${_user}' has full access on '${_userdb}'"

echo "enjoy!"
echo "========================================================================"

mysqladmin -uroot shutdown
