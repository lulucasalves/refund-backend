SET GLOBAL log_bin_trust_function_creators = 1;

CREATE TABLE IF NOT EXISTS companyStatus (
    statusId CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    status VARCHAR(50) NOT NULL,
    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO companyStatus (statusId, status) VALUES ("c0246355-2708-11f0-9bf9-0242ac130002", "active");
INSERT INTO companyStatus (status) VALUES ("inactive");

CREATE TABLE IF NOT EXISTS currency (
    currencyId CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    symbol VARCHAR(10) NOT NULL,
    country VARCHAR(100) NOT NULL,
    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO currency (symbol, country) VALUES ('R$', 'BR');
INSERT INTO currency (symbol, country) VALUES ('$', 'US');

CREATE TABLE IF NOT EXISTS dateFormat (
    dateFormatId CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    dateFormat VARCHAR(10) NOT NULL,
    country VARCHAR(2) NOT NULL,
    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO dateFormat (dateFormat, country) VALUES ('DD/MM/YYYY', "BR");
INSERT INTO dateFormat (dateFormat, country) VALUES ('MM/DD/YYYY', "US");

CREATE TABLE IF NOT EXISTS ambient (
    ambientId CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(100) NOT NULL,
    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS company (
    companyId CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(100) NOT NULL,
    statusId CHAR(36) NOT NULL,
    currencyId CHAR(36) NOT NULL,
    dateFormatId CHAR(36) NOT NULL,
    ambientId CHAR(36) NOT NULL,
    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (statusId) REFERENCES companyStatus(statusId),
    FOREIGN KEY (currencyId) REFERENCES currency(currencyId),
    FOREIGN KEY (dateFormatId) REFERENCES dateFormat(dateFormatId),
    FOREIGN KEY (ambientId) REFERENCES ambient(ambientId),
    UNIQUE KEY (name, ambientId)
);

CREATE TABLE IF NOT EXISTS user (
    userId CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    profilePicture VARCHAR(255),
    lastLogin TIMESTAMP NULL,
    lastAmbientId CHAR(36) NULL,
    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS userCompany (
    userCompanyId CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    userId CHAR(36) NOT NULL,
    companyId CHAR(36) NOT NULL,
    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userId) REFERENCES user(userId),
    FOREIGN KEY (companyId) REFERENCES company(companyId),
    UNIQUE KEY (userId, companyId)
);

CREATE TABLE IF NOT EXISTS eventStatus (
    statusId CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    status VARCHAR(50) NOT NULL,
    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO eventStatus (statusId, status) VALUES ("3fc5627a-2127-4cfb-a94f-e47f4d5ec77d", "active");
INSERT INTO eventStatus (status) VALUES ("inactive");

CREATE TABLE IF NOT EXISTS event (
    eventId CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(100) NOT NULL,
    statusId CHAR(36) NOT NULL,
    startDate DATETIME NOT NULL,
    endDate DATETIME NOT NULL,
    companyId CHAR(36) NOT NULL,
    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (statusId) REFERENCES eventStatus(statusId),
    FOREIGN KEY (companyId) REFERENCES company(companyId),
    UNIQUE KEY (name, companyId)
);

CREATE TABLE IF NOT EXISTS employee (
    employeeId CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(30),
    document VARCHAR(30),
    verification VARCHAR(30) NOT NULL,
    userId CHAR(36) NOT NULL,
    companyId CHAR(36) NOT NULL,
    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (userId) REFERENCES user(userId),
    FOREIGN KEY (companyId) REFERENCES company(companyId),
    UNIQUE KEY (userId, companyId)
);

CREATE TABLE IF NOT EXISTS employeeInvite (
    employeeInviteId CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    status VARCHAR(30) NOT NULL,
    employeeId CHAR(36) NOT NULL,
    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (employeeId) REFERENCES employee(employeeId),
    UNIQUE KEY (employeeId)
);

CREATE TABLE IF NOT EXISTS userGroup (
    userGroupId CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(100) NOT NULL,
    can_modify TINYINT(1) DEFAULT 0,
    companyId CHAR(36) NOT NULL,
    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (companyId) REFERENCES company(companyId),
    UNIQUE KEY (companyId, name)
);

CREATE TABLE IF NOT EXISTS userGroupEmployee (
    userGroupEmployeeId CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    userGroupId CHAR(36) NOT NULL,
    employeeId CHAR(36) NOT NULL,
    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (userGroupId) REFERENCES userGroup(userGroupId),
    FOREIGN KEY (employeeId) REFERENCES employee(employeeId),
    UNIQUE KEY (userGroupId, employeeId)
);

CREATE TABLE IF NOT EXISTS role (
    roleId CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(100) NOT NULL,
    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY (roleId, name)
);

INSERT INTO role (name) VALUES ('editAmbient'); -- Consegue editar nome do ambiente
INSERT INTO role (name) VALUES ('editRole'); -- Consegue gerir permissões

INSERT INTO role (name) VALUES ('viewEmployee'); -- Consegue ver apenas ele se tiver desabilitado
INSERT INTO role (name) VALUES ('editEmployee'); -- Consegue editar apenas seu usuário
INSERT INTO role (name) VALUES ('manageEmployee'); -- Consegue gerir outros funcionários

INSERT INTO role (name) VALUES ('viewUserGroup');
INSERT INTO role (name) VALUES ('editUserGroup');

INSERT INTO role (name) VALUES ('viewEvent'); -- Consegue ver apenas o seu reembolso
INSERT INTO role (name) VALUES ('editEvent'); -- Consegue editar eventos

INSERT INTO role (name) VALUES ('viewCompany'); -- Consegue ver apenas a empresa adicionado na seleção de empresas
INSERT INTO role (name) VALUES ('editCompany');

INSERT INTO role (name) VALUES ('viewRefund'); -- Consegue ver apenas o seu reembolso se desabilitado
INSERT INTO role (name) VALUES ('editRefund'); -- Consegue editar apenas seu reembolso
INSERT INTO role (name) VALUES ('manageRefund'); -- Consegue editar reembolso dos outros
INSERT INTO role (name) VALUES ('approveRefund'); -- Consegue aprovar reembolso dos outros

CREATE TABLE IF NOT EXISTS userGroupRole (
    userGroupRoleId CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    userGroupId CHAR(36) NOT NULL,
    roleId CHAR(36) NOT NULL,
    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (userGroupId) REFERENCES userGroup(userGroupId),
    FOREIGN KEY (roleId) REFERENCES role(roleId),
    UNIQUE KEY (userGroupId, roleId)
);