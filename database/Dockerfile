FROM mariadb:latest

ENV MYSQL_ROOT_PASSWORD=mysql
ENV MYSQL_DATABASE=authentication
ENV MYSQL_USER=authentication
ENV MYSQL_PASSWORD=authenticationpass

ADD authentication-schema.sql /docker-entrypoint-initdb.d

EXPOSE 3306