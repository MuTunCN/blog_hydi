drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  'text' text not null,
  'update' datetime not null,
  clicked INTEGER not null,
  tag text not NULL ,
  category text not NULL ,
    FOREIGN key (tag) REFERENCES tag(tag)
    FOREIGN KEY (category) REFERENCES category(category)
);

DROP TABLE if EXISTS tag;
create table tag (
  tag text not null
);

DROP TABLE if EXISTS category;
create table category (
  category text not NULL
);

INSERT INTO tag VALUES ("tag_text");
INSERT INTO category VALUES ("category_text");
INSERT INTO entries VALUES (1, "title", "text", "2017.7.10", 30, "tag_text", "category_text");