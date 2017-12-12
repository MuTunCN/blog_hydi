drop table if exists post;
create table post (
  id integer primary key autoincrement,
  title text not null,
  body text not null,
  up_date datetime not null,
  clicked INTEGER not null,
  category_id INTEGER not NULL ,
    FOREIGN KEY (category_id) REFERENCES category(id)
);

DROP TABLE if EXISTS tag;
create table tag (
  id INTEGER PRIMARY KEY autoincrement,
  name text not null
);

DROP TABLE if EXISTS category;
create table category (
  id INTEGER PRIMARY KEY autoincrement,
  name text not NULL
);

DROP TABLE if EXISTS tags;
CREATE TABLE tags(
  id INTEGER PRIMARY KEY AUTOINCREMENT ,
  tag_id INTEGER  ,
  post_id INTEGER
);

