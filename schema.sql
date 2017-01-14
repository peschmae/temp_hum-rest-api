drop table if exists temperature;
create table temperature (
  id integer primary key autoincrement,
  temp float not null,
);
create table humidity (
  id integer primary key autoincrement,
  hum float not null,
);