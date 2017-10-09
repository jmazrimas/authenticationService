FROM mariadb:latest

# Define environment variable

ARG auth_svc_root_db_pass
ARG auth_svc_db_name
ARG auth_svc_db_user
ARG auth_svc_db_pass

ENV MYSQL_ROOT_PASSWORD=$auth_svc_root_db_pass
ENV MYSQL_DATABASE=$auth_svc_db_name
ENV MYSQL_USER=$auth_svc_db_user
ENV MYSQL_PASSWORD=$auth_svc_db_pass