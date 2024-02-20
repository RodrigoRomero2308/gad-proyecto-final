create type arraydos as (arr numeric[]);
create type arraytres as (arr arraydos[]);

create table if not exists "range" (
	"id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
	"lower_distance" NUMERIC,
	"upper_distance" NUMERIC
);