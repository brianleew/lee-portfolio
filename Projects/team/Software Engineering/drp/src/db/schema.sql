CREATE TABLE IF NOT EXISTS entities (
    entity_id INT AUTO_INCREMENT PRIMARY KEY,
    entity_type ENUM('user', 'organization')
);

CREATE TABLE IF NOT EXISTS organizations (
    org_id INT PRIMARY KEY,
    org_name VARCHAR(50) NOT NULL UNIQUE,
    coordinates POINT,
    FOREIGN KEY (org_id) REFERENCES entities(entity_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS users (
	account_id INT PRIMARY KEY,
    email VARCHAR(254) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    org_id INT,
    approval_status ENUM('Pending', 'Approved', 'Rejected', 'Admin') DEFAULT 'Pending',
    FOREIGN KEY (account_id) REFERENCES entities(entity_id) ON DELETE CASCADE,
    FOREIGN KEY (org_id) REFERENCES organizations(org_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS logins (
    account_id INT NOT NULL,
    password_hash VARCHAR(64) NOT NULL,
    FOREIGN KEY (account_id) REFERENCES users(account_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS meters (
    meter_id INT PRIMARY KEY,
    coordinates POINT
);

CREATE TABLE IF NOT EXISTS meter_data (
	meter_id INT NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    meter_value DECIMAL(8,2),
    prediction_value DECIMAL(8,2),
    delta_value DECIMAL(8,2),
    FOREIGN KEY (meter_id) REFERENCES meters(meter_id) ON DELETE CASCADE,
    UNIQUE (meter_id, start_time, end_time)
);

CREATE TABLE IF NOT EXISTS meter_map (
    entity_id INT NOT NULL,
    meter_id INT NOT NULL,
    FOREIGN KEY (entity_id) REFERENCES entities(entity_id) ON DELETE CASCADE,
    FOREIGN KEY (meter_id) REFERENCES meters(meter_id) ON DELETE CASCADE,
    UNIQUE (entity_id, meter_id)
);

CREATE TABLE IF NOT EXISTS sessions (
    session_id UUID PRIMARY KEY,
    account_id INT NOT NULL,
    session_expire DATETIME NOT NULL,
    FOREIGN KEY (account_id) REFERENCES users(account_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS drp_periods (
    drp_id INT AUTO_INCREMENT PRIMARY KEY,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL
);
