-- 데이터베이스 생성
CREATE DATABASE animallens;

-- 테이블 생성
\c animallens

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

-- 초기 동물 데이터 삽입
INSERT INTO animals (name, species, habitat, diet, description) VALUES
('Lion', 'Panthera leo', 'African savannas', 'Carnivore', 'The lion is the king of the jungle...'),
('Tiger', 'Panthera tigris', 'Asian forests', 'Carnivore', 'The largest of all wild cats...'),
('Elephant', 'Loxodonta africana', 'African savannas and forests', 'Herbivore', 'The largest land animal...'),
('Giraffe', 'Giraffa camelopardalis', 'African savannas', 'Herbivore', 'The tallest land animal...'); 