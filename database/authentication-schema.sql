DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id int(11) NOT NULL AUTO_INCREMENT,
  name varchar(100) NOT NULL,
  tp_name varchar(100) NOT NULL,
  tp_id varchar(100) NOT NULL,
  access_key varchar(100) NOT NULL,
  renew_key varchar(100) NOT NULL,
  session varchar(100) NOT NULL,
  expire_time timestamp NOT NULL,
  PRIMARY KEY (id)
);