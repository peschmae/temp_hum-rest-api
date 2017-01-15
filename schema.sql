drop table if exists temp_hum_records;
create table temp_hum_records (
  id integer primary key auto_increment,
  tstamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  temp float not null,
  hum float not null
);