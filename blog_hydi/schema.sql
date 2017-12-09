drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  'text' text not null,
  'update' datetime not null,
  clicked INTEGER not null,
  tag_id INTEGER not NULL ,
  category_id INTEGER not NULL ,
    FOREIGN key (tag_id) REFERENCES tag(id),
    FOREIGN KEY (category_id) REFERENCES category(id)
);

DROP TABLE if EXISTS tag;
create table tag (
  id INTEGER PRIMARY KEY autoincrement,
  tag text not null
);

DROP TABLE if EXISTS category;
create table category (
  id INTEGER PRIMARY KEY autoincrement,
  category text not NULL
);

INSERT INTO tag VALUES (1,"tag_text");
INSERT INTO category VALUES (1,"category_text");
INSERT INTO entries VALUES (1,"title", "text", "2017.7.10", 30, 1, 1);