drop table if exists users;
create table users (
    id integer primary key autoincrement,
    rabid varchar not null,
    short_id text not null
);

drop table if exists citations;
create table citations (
    id integer primary key autoincrement,
    rabid varchar not null,
    user_rabid varchar not null,
    display_string text not null,
    style_rabid varchar not null,
    featured boolean not null,
    rank integer not null,
    FOREIGN KEY(user_rabid) REFERENCES users(rabid),
    FOREIGN KEY(style_rabid) REFERENCES citation_styles(rabid)
);

drop table if exists citation_exids;
create table citation_exids (
    id integer primary key autoincrement,
    citation_rabid varchar not null,
    exid varchar not null,
    domain varchar not null,
    FOREIGN KEY(citation_rabid) REFERENCES citations(rabid)
);

drop table if exists citation_styles;
create table citation_styles (
    id integer primary key autoincrement,
    rabid varchar not null,
    template text not null
);

drop table if exists harvest_exids;
create table harvest_exids (
    id integer primary key autoincrement,
    exid varchar not null,
    event_id integer not null,
    user_rabid varchar not null,
    source_rabid varchar not null,
    status varchar not null,
    FOREIGN KEY(event_id) REFERENCES harvest_events(id),
    FOREIGN KEY(source_rabid) REFERENCES harvest_sources(rabid),
    FOREIGN KEY(user_rabid) REFERENCES users(rabid)
);

drop table if exists harvest_events;
create table harvest_events (
    id integer primary key autoincrement,
    proc_rabid varchar not null,
    event_date date not null,
    user_initiated boolean not null,
    FOREIGN KEY(proc_rabid) REFERENCES harvest_proc(rabid)
);

drop table if exists harvest_processes;
create table harvest_processes (
    id integer primary key autoincrement,
    rabid varchar not null,
    display varchar not null,
    rabclass varchar not null,
    status varchar not null,
    user_rabid varchar not null,
    source_rabid varchar not null,
    FOREIGN KEY(source_rabid) REFERENCES harvest_sources(rabid),
    FOREIGN KEY(user_rabid) REFERENCES users(rabid)
);

drop table if exists harvest_sources;
create table harvest_sources (
    id integer primary key autoincrement,
    rabid varchar not null,
    display varchar not null,
    rabclass varchar not null
);

create index user_rabids on users(rabid);
create index citation_rabids on citations(rabid);
create index style_rabids on citation_styles(rabid);
create index proc_rabids on harvest_processes(rabid);
create index source_rabids on harvest_sources(rabid);
