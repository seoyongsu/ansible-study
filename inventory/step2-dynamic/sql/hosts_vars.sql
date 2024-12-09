create table hosts_vars(
    ip VARCHAR(15) NOT NULL,
    `keys` VARCHAR(255),
    `VALUES` VARCHAR(255),

    INDEX IDX_01 (ip)
);

INSERT INTO hosts_vars(ip, `keys`, `values`)
VALUES
    ('172.17.0.4', 'ansible_user', 'root'),
    ('172.17.0.7', 'ansible_user', 'root'),
    ('172.17.0.7', 'ansible_password', '1234');