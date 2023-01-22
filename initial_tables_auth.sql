CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
   id uuid DEFAULT uuid_generate_v4(),
   username VARCHAR NOT NULL,
   password VARCHAR NOT NULL,
   PRIMARY KEY (id)
);

INSERT INTO "users" ("username", "password")
VALUES ('maistodos', 'pbkdf2:sha256:1000$Va9cNZvBGgNF9Xd9$c0d9730a1bac5d48711396edc054d3c04015c514bfa23c26d132b68962f63ad4');
