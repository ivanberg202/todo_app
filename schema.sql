CREATE TABLE users (
	id INTEGER NOT NULL, 
	email VARCHAR, 
	username VARCHAR, 
	first_name VARCHAR, 
	last_name VARCHAR, 
	hashed_password VARCHAR, 
	is_active BOOLEAN, 
	role VARCHAR, 
	PRIMARY KEY (id), 
	UNIQUE (email), 
	UNIQUE (username)
);
CREATE INDEX ix_users_id ON users (id);
CREATE TABLE todos (
	id INTEGER NOT NULL, 
	title VARCHAR, 
	description VARCHAR, 
	priority INTEGER, 
	complete BOOLEAN, 
	owner_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(owner_id) REFERENCES users (id)
);
CREATE INDEX ix_todos_id ON todos (id);
CREATE TABLE todosapp (
	id INTEGER NOT NULL, 
	title VARCHAR, 
	description VARCHAR, 
	priority INTEGER, 
	complete BOOLEAN, 
	owner_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(owner_id) REFERENCES users (id)
);
CREATE INDEX ix_todosapp_id ON todosapp (id);
