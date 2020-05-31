create schema saberbot;

create table pnts(
	id_pontos int not null auto_increment,
    nome varchar(100) not null,
    pontos int not null default 0,
    server bigint not null,
    primary key (id_pontos)
);

create table adm_roles(
	server bigint not null,
    id_role bigint not null,
    primary key (server)
);

create table status_api(
	id int not null auto_increment,
	rand int not null,
    disc int not null,
    primary key(id)
);

create table aviso(
	id int not null auto_increment,
	server bigint not null,	
    user bigint not null,
    expires datetime not null,
    primary key(id)
);

create table mute(
	id int not null auto_increment,
	server bigint not null,	
    user bigint not null,
    expires datetime not null,
    primary key(id)
);