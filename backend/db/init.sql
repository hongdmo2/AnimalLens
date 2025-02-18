-- warning: this script is only executed once for initial database setup.
-- re-running it may delete existing data.
-- purpose
-- create database
-- create tables
-- insert initial animal data


-- create database
-- only run once
--CREATE DATABASE animallens;

-- create tables
CREATE TABLE animals (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    species VARCHAR(100),
    habitat TEXT,
    diet TEXT,
    description TEXT
);

CREATE TABLE analysis_results (
    id SERIAL PRIMARY KEY,
    image_url TEXT NOT NULL,
    label VARCHAR(100),
    confidence DECIMAL(5, 2),
    matched_animal_id INTEGER REFERENCES animals(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- insert initial animal data
INSERT INTO animals (name, species, habitat, diet, description) VALUES
('Lion', 'Panthera leo', 'African savannas', 'Carnivore', 'The lion is the king of the jungle...'),
('Tiger', 'Panthera tigris', 'Asian forests', 'Carnivore', 'The largest of all wild cats...'),
('Elephant', 'Loxodonta africana', 'African savannas and forests', 'Herbivore', 'The largest land animal...'),
('Giraffe', 'Giraffa camelopardalis', 'African savannas', 'Herbivore', 'The tallest land animal...'); 