drop table if exists users;
create table users (
    id integer primary key autoincrement,
    rabid text not null,
    short_id text not null
);

drop table if exists citations;
create table citations (
    id integer primary key autoincrement,
    rabid text not null,
    user_rabid text not null,
    display_string text not null,
    style_rabid text not null,
    featured boolean not null,
    rank integer not null,
    FOREIGN KEY(user_rabid) REFERENCES users(rabid),
    FOREIGN KEY(style_rabid) REFERENCES citation_styles(rabid)
);

drop table if exists citation_exids;
create table citation_exids (
    id integer primary key autoincrement,
    citation_id text not null,
    exid text not null,
    domain text not null,
    FOREIGN KEY(citation_id) REFERENCES citations(id)
);

drop table if exists citation_styles;
create table citation_styles (
    id integer primary key autoincrement,
    rabid text not null,
    template text not null
);

drop table if exists harvest_records;
create table harvest_records (
    id integer primary key autoincrement,
    user_rabid text not null,
    venue text not null,
    title text not null,
    date text not null,
    status text not null,
    FOREIGN KEY(user_rabid) REFERENCES users(rabid)
);

drop table if exists harvest_record_exids;
create table harvest_record_exids (
    id integer primary key autoincrement,
    record_id text not null,
    exid text not null,
    domain text not null,
    FOREIGN KEY(record_id) REFERENCES harvest_records(id)
);

drop table if exists harvest_query;
create table harvest_queries (
    id integer primary key autoincrement,
    rabid text not null,
    user_rabid text not null,
    query_string text not null,
    FOREIGN KEY(user_rabid) REFERENCES users(rabid)
);