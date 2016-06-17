CREATE KEYSPACE justbid WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' :3};
USE justbid;

CREATE TABLE user_item(
    user_id text,
    item_id text,
    PRIMARY KEY (user_id, item_id)
);


CREATE TABLE simpletable (
  item bigint,
  name bigint,
  PRIMARY KEY (item)
);
