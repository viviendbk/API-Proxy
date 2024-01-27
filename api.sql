-- Customer table
DROP TABLE IF EXISTS customer;
CREATE TABLE customer(
    customerId INT PRIMARY KEY,
    pseudo VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    password VARCHAR(255) NOT NULL
);

-- Proxy table
DROP TABLE IF EXISTS proxy;
CREATE TABLE proxy(
    proxyId INT PRIMARY KEY,
    ip VARCHAR(255) NOT NULL,
    port INT NOT NULL,
    type VARCHAR(255) NOT NULL,
    interface VARCHAR(255) NOT NULL
);

-- CustomerProxy table
DROP TABLE IF EXISTS customerProxy;
CREATE TABLE customerProxy(
    customerId INT,
    proxyId INT,
    endDate DATE NOT NULL,
    usedFor VARCHAR(255) NOT NULL,
    PRIMARY KEY (customerId, proxyId),
    FOREIGN KEY (customerId) REFERENCES customer(customerId),
    FOREIGN KEY (proxyId) REFERENCES proxy(proxyId)
);


-- get proxy unnasigned
SELECT * FROM proxy
WHERE proxyId NOT IN (
    SELECT proxyId FROM customerproxy
)
OR proxyId IN (
    SELECT proxyId FROM customerproxy
    WHERE endDate > NOW()
);

-- get proxy unnasigned for a specific use
SELECT * FROM proxy
WHERE proxyId NOT IN (
    SELECT proxyId FROM customerproxy
    WHERE usedFor != :usedFor
);

-- get proxy unnasigned for a specific use
SELECT p."proxyId", "ip", "port", "type", "interface", "endDate", "usedFor" FROM "Proxy" p 
LEFT JOIN "CustomerProxy" cp ON p."proxyId" = cp."proxyId" 
WHERE cp."customerId" = :customerId



--sample insertion
-- Inserting into the 'customer' table
INSERT INTO customer (customerId, pseudo, email, password) VALUES
  (1, 'john_doe', 'john.doe@example.com', 'password123'),
  (2, 'alice_smith', 'alice.smith@example.com', 'securepass'),
  (3, 'bob_jones', 'bob.jones@example.com', 'pass123');

-- Inserting into the 'proxy' table
INSERT INTO proxy (proxyId, ip, port, type, interface) VALUES
  (1, '192.168.1.1', 8080, 'HTTP', 'eth0'),
  (2, '10.0.0.2', 8888, 'HTTPS', 'eth1'),
  (3, '172.16.0.3', 3128, 'SOCKS5', 'eth2');

-- Inserting into the 'customerproxy' table
INSERT INTO customerproxy (customerId, proxyId, endDate, usedFor) VALUES
  (1, 1, '2024-02-01', 'Dofus'),
  (2, 2, '2024-03-15', 'Dofus'),
  (3, 2, '2024-04-20', 'Scrapping');
