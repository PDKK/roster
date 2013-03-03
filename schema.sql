drop table if exists entries;
create table entries (
      id integer primary key autoincrement,
      name string not null,
      age integer not null,
      club string,
      category integer not null,
      time real,
      history string
);

drop table if exists categories;
create table categories (
       id integer primary key autoincrement,
       name string not null
);

insert into categories (name) values ("Men"), ("Women"), ("Under 16");
