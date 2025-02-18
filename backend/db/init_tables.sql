-- warning: this script is only executed once for initial table setup.
-- if table structure needs to be changed, use migrate.py.
-- purpose
-- define table schema
-- set up table relationships


-- delete existing tables
DROP TABLE IF EXISTS analysis_results CASCADE;
DROP TABLE IF EXISTS unidentified_animals CASCADE;
DROP TABLE IF EXISTS animals CASCADE;

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

-- table to save unidentified animals
CREATE TABLE unidentified_animals (
    id SERIAL PRIMARY KEY,
    label VARCHAR(100) NOT NULL,
    confidence DECIMAL(5, 2),
    image_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR(50) DEFAULT 'pending'  -- pending, approved, rejected
);

-- insert initial animal data
INSERT INTO animals (name, species, habitat, diet, description) VALUES
('Lion', 'Panthera leo', 'African savannas', 'Carnivore', 'The lion is the king of the jungle...'),
('Tiger', 'Panthera tigris', 'Asian forests', 'Carnivore', 'The largest of all wild cats...'),
('Elephant', 'Loxodonta africana', 'African savannas and forests', 'Herbivore', 'The largest land animal...'),
('Giraffe', 'Giraffa camelopardalis', 'African savannas', 'Herbivore', 'The tallest land animal...'),
('Cat', 'Felis catus', 'Domestic environments', 'Carnivore', 'Common household pet known for independence...'),
('Dog', 'Canis lupus familiaris', 'Domestic environments', 'Omnivore', 'Loyal companion animal...'),
('Bear', 'Ursidae', 'Forests and mountains', 'Omnivore', 'Large powerful mammals...'),
('Panda', 'Ailuropoda melanoleuca', 'Chinese bamboo forests', 'Herbivore', 'Black and white bear native to China...'); 