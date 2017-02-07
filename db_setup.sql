CREATE TABLE posts (id serial primary key, content text, time timestamp default now());
CREATE TABLE posts_bad (id integer references posts, unsanitized_content text);
