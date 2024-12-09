create table hosts_group_vars(
    group_name VARCHAR(255) default 'ALL',
    `keys` VARCHAR(255),
    `values` VARCHAR(255),

    INDEX IDX_01 (group_name)
);

INSERT INTO hosts_group_vars(group_name, `keys`, `values`)
VALUES
    ('dbservers', 'ansible_user','root'),
    ('dbservers', 'ansible_password','db_userpass');