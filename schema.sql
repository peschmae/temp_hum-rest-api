drop table if exists temperature;
create table temperature (
  id integer primary key auto_increment,
  temp float not null
);
drop table if exists humidity;
create table humidity (
  id integer primary key auto_increment,
  hum float not null
);