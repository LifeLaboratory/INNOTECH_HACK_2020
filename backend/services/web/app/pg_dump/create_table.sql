create table client
(
    client_id         serial not null
        constraint client_pk
            primary key,
    surname           text,
    name              text,
    patronymic        text,
    nationality       text,
    country           text,
    inn               bigint,
    inn_reg           date,
    link_vk           text,
    sex               integer,
    phone             bigint,
    bdate             date,
    site              text,
    city              text,
    link_example_face text
);

comment on table client is 'Клиенты банка';

alter table client owner to postgres;

create unique index client_id_uindex
	on client (client_id);
	

create table interests
(
	interest_id serial not null
		constraint interests_pk
			primary key,
	interest_name text
);

create table organization
(
	organization_id serial not null
		constraint organization_pk
			primary key,
	organization_name text,
	organization_url text,
	organization_status text,
	organization_leader text,
	organization_date_reg date,
	organization_inn bigint
);

alter table organization owner to postgres;

create unique index organization_id_uindex
	on organization (organization_id);
	
create table terrorists
(
	id serial not null
		constraint terrorists_pk
			primary key,
	surname text,
	name text,
	patronymic text,
	date_birth date,
	place_birth text
);

comment on table terrorists is 'Перечень террористов или экстремистов';

alter table terrorists owner to postgres;

create unique index terrorists_id_uindex
	on terrorists (id);

create table link_client_interest
(
	client_id integer not null
		constraint link_client_interest_client_id_fkey
			references client,
	interest_id integer not null
		constraint link_client_interest_interest_id_fkey
			references interests,
	constraint link_client_interest_pkey
		primary key (client_id, interest_id)
);

comment on table link_client_interest is 'Связь клиентов и организаций';

alter table link_client_interest owner to postgres;

create table link_client_organization
(
	client_id integer not null
		constraint link_client_organization_client_id_fkey
			references client,
	organization_id integer not null
		constraint link_client_organization_organization_id_fkey
			references organization,
	status_client text,
	constraint link_client_organization_pkey
		primary key (client_id, organization_id)
);

alter table link_client_organization owner to postgres;

create table category
(
    id         serial not null
        constraint category_pk
            primary key,
    "Название" text
);

comment on table category is 'Категории клиентов';

alter table category owner to postgres;

create unique index category_id_uindex
    on category (id);

create table link_client_category
(
    id          serial  not null
        constraint link_client_category_pk
            primary key,
    client_id   integer not null,
    category_id integer not null
);

alter table link_client_category owner to postgres;

create unique index link_client_category_id_uindex
    on link_client_category (id);

