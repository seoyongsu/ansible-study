CREATE TABLE hosts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ip VARCHAR(15) NOT NULL,
    host_name VARCHAR(255),
    group_name VARCHAR(255)
);

INSERT INTO hosts(ip, host_name, group_name)
VALUES
    ('172.17.0.2', 	NULL, 		null),
    ('172.17.0.3', 	'default1', 	NULL),
    ('172.17.0.4', 	'default2', 	NULL),
    ('172.17.0.5', 	NULL, 		'webservers'),
    ('172.17.0.6', 	'web1', 	'webservers'),
    ('172.17.0.7', 	'web2', 	'webservers'),
    ('172.17.0.8', 	NULL, 		'dbservers'),
    ('172.17.0.9', 	'db2', 		'dbservers');