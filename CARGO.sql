create database cargo;
USE cargo;

-- Table for Admin
CREATE TABLE Admin (
    admin_id VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    admin_name VARCHAR(255) NOT NULL
);


-- Table for Port
CREATE TABLE Port (
    port_id INT AUTO_INCREMENT PRIMARY KEY,
    port_name VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    address VARCHAR(255),
    admin_id VARCHAR(255),
    FOREIGN KEY (admin_id) REFERENCES Admin(admin_id)
);

-- Table for OriginPort
CREATE TABLE OriginPort (
    origin_port_id INT AUTO_INCREMENT PRIMARY KEY,
    port_id INT,
    admin_id VARCHAR(255),
    FOREIGN KEY (admin_id) REFERENCES Admin(admin_id),
    FOREIGN KEY (port_id) REFERENCES Port(port_id)
);

-- Table for DestinationPort
CREATE TABLE DestinationPort (
    destination_port_id INT AUTO_INCREMENT PRIMARY KEY,
    port_id INT,
    admin_id VARCHAR(255),
    FOREIGN KEY (admin_id) REFERENCES Admin(admin_id),
    FOREIGN KEY (port_id) REFERENCES Port(port_id)
);
-- Table for Route
CREATE TABLE Route (
    route_id INT AUTO_INCREMENT PRIMARY KEY,
    origin_port_id INT,
    destination_port_id INT,
    admin_id VARCHAR(255),
    FOREIGN KEY (origin_port_id) REFERENCES OriginPort(origin_port_id),
    FOREIGN KEY (destination_port_id) REFERENCES DestinationPort(destination_port_id),
    FOREIGN KEY (admin_id) REFERENCES Admin(admin_id)
);

-- Table for Customer
CREATE TABLE Customer (
    customer_id VARCHAR(255) NOT NULL PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    address VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    admin_id VARCHAR(255) NOT NULL,
    FOREIGN KEY (admin_id) REFERENCES Admin(admin_id)
);

-- Table for Ship
CREATE TABLE Ship (
    ship_id INT AUTO_INCREMENT PRIMARY KEY,
    ship_name VARCHAR(255) NOT NULL,
    arrival_date DATE,
    departure_date DATE,
    route_id INT,
    admin_id VARCHAR(255),
    max_storage INT,
    current_storage INT ,
    FOREIGN KEY (route_id) REFERENCES Route(route_id),
    FOREIGN KEY (admin_id) REFERENCES Admin(admin_id)
);

-- Table for Cargo
CREATE TABLE Cargo (
    cargo_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id VARCHAR(255),
    cargo_name VARCHAR(255),
    ship_id INT,
    cargo_type VARCHAR(255),
    route_id INT,
    admin_id VARCHAR(255),
    weight_in_tons INT,
    INDEX (admin_id),
    FOREIGN KEY (route_id) REFERENCES Route(route_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (ship_id) REFERENCES Ship(ship_id)
);

-- Trigger to set default value for current_storage to 0 in Ship table
DELIMITER //
CREATE TRIGGER before_ship_insert
BEFORE INSERT ON Ship
FOR EACH ROW
BEGIN
    SET NEW.current_storage = 2;
END;
//
DELIMITER ;

-- Create a stored procedure to get customer information along with origin and destination port names
DELIMITER //

CREATE PROCEDURE GetCustomerInfo(
    IN p_customer_id VARCHAR(255)
)
BEGIN
    SELECT
        C.customer_id,
        C.customer_name,
        AOPort.port_name AS origin_port_name,
        ADPort.port_name AS destination_port_name,
        CR.cargo_name AS cargo_name
        CR.ship_id AS SHIP_ID
    FROM
        Customer C
    JOIN
        Cargo CR ON C.customer_id = CR.customer_id
    JOIN
        Route R ON CR.route_id = R.route_id
    JOIN
        OriginPort OPort ON R.origin_port_id = OPort.origin_port_id
    JOIN
        DestinationPort DPort ON R.destination_port_id = DPort.destination_port_id
    JOIN
        Port AOPort ON OPort.port_id = AOPort.port_id
    JOIN
        Port ADPort ON DPort.port_id = ADPort.port_id
    WHERE
        C.customer_id = p_customer_id;
END //

DELIMITER ;
DELIMITER //

DROP PROCEDURE IF EXISTS GetCustomerInfo;

DELIMITER ;


