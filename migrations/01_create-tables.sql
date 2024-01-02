
create table if not exists users (
    id integer primary key autoincrement,
    username varchar(255) not null unique,
    password varchar(50) not null,
    vlan_id integer not null
);

create table if not exists restrictions (
    id integer primary key autoincrement,
    type varchar not null,
    blocked_ip varchar(20) not null,
    blocked_port integer not null,
    blocked_user_id integer references users(id),
    blocked_vlan_id integer,
    description text
);