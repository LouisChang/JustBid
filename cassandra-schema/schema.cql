CREATE KEYSPACE justbid WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' :3};
USE justbid;

CREATE TABLE bidding3(
    item_id bigint,
    user_id bigint,
    bid_price bigint,
    current_time text,
    time timestamp,
    PRIMARY KEY (item_id,time)
) WITH CLUSTERING ORDER BY (time DESC);

CREATE TABLE bidding_user(
    item_id bigint,
    user_id bigint,
    bid_price bigint,
    current_time text,
    time timestamp,
    PRIMARY KEY (user_id,time)
) WITH CLUSTERING ORDER BY (time DESC);

CREATE TABLE recommendation(
    user_id bigint,
    recom_id bigint
    PRIMARY KEY (user_id)
);


