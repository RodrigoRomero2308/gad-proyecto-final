create table if not exists "bird_song" (
	"id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
	"filename" VARCHAR NOT NULL,
	"vector" INT4[] NOT NULL DEFAULT array[]::int4[],
	"common_name" VARCHAR,
	"species" VARCHAR
);
