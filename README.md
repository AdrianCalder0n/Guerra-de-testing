Necesitas xamp
Activar mysql y apache
crear base de datos con esto

CREATE DATABASE IF NOT EXISTS inventario;

USE inventario;

CREATE TABLE IF NOT EXISTS usuarios (
  id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(75) NOT NULL,
  password VARCHAR(75) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS productos (
  id INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(75) NOT NULL,
  precio FLOAT(10,2) NOT NULL,
  stock INT NOT NULL,
  PRIMARY KEY (id)
);

INSERT INTO usuarios (username, password) VALUES 
('brayton', 'brayton'),
('gina', 'gina'),
('rodrigo', 'rodrigo'),
('alex', 'alex'),
('adrian', 'adrian');

INSERT INTO productos (nombre, precio, stock) VALUES 
('Martillo', 40.00, 20),
('Destornillador plano', 20.00, 30),
('Destornillador de estrella', 25.00, 25),
('Cinta métrica', 30.00, 15),
('Pintura en aerosol (negra)', 15.00, 10),
('Pintura en aerosol (blanca)', 15.00, 12),
('Taladro eléctrico', 360.00, 8),
('Sierra eléctrica', 500.00, 5),
('Clavos (1 pulgada)', 12.00, 40),
('Llave ajustable', 30.00, 20);

En tu terminal instalar las siguientes librerias

pip install virtualenv
pip install flask
pip install Flask Flask-Login
pip install mysql-connector-python
