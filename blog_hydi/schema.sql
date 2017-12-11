drop table if exists post;
create table post (
  id integer primary key autoincrement,
  title text not null,
  body text not null,
  up_date text not null,
  clicked INTEGER not null,
  tag_id INTEGER not NULL ,
  category_id INTEGER not NULL ,
    FOREIGN key (tag_id) REFERENCES tag(id),
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

INSERT INTO tag VALUES (1,"tag_text");
INSERT INTO category VALUES (1,"category_text");
INSERT INTO post VALUES (1,"title", "text", "20171212", 30, 1, 1);