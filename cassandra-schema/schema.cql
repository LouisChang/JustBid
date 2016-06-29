CREATE KEYSPACE justbid WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' :3};
USE justbid;

CREATE TABLE bidding2(
    item_id bigint,
    user_id bigint,
    bid_price bigint,
    PRIMARY KEY (item_id,user_id)
);


CREATE TABLE simpletable (
  item bigint,
  name bigint,
  PRIMARY KEY (item)
);
