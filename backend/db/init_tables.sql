-- 주의: 이 스크립트는 최초 테이블 설정 시 한 번만 실행합니다.
-- 테이블 구조 변경이 필요한 경우 migrate.py를 사용하세요.
--목적
--테이블 스키마 정의
--테이블 간 관계 설정


-- 기존 테이블 삭제
DROP TABLE IF EXISTS analysis_results;
DROP TABLE IF EXISTS animals;

-- 테이블 생성
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

-- 미확인 동물 저장 테이블
CREATE TABLE unidentified_animals (
    id SERIAL PRIMARY KEY,
    label VARCHAR(100) NOT NULL,
    confidence DECIMAL(5, 2),
    image_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR(50) DEFAULT 'pending'  -- pending, approved, rejected
);

-- 초기 동물 데이터 삽입
INSERT INTO animals (name, species, habitat, diet, description) VALUES
('Lion', 'Panthera leo', 'African savannas', 'Carnivore', 'The lion is the king of the jungle...'),
('Tiger', 'Panthera tigris', 'Asian forests', 'Carnivore', 'The largest of all wild cats...'),
('Elephant', 'Loxodonta africana', 'African savannas and forests', 'Herbivore', 'The largest land animal...'),
('Giraffe', 'Giraffa camelopardalis', 'African savannas', 'Herbivore', 'The tallest land animal...'),
('Cat', 'Felis catus', 'Domestic environments', 'Carnivore', 'Common household pet known for independence...'),
('Dog', 'Canis lupus familiaris', 'Domestic environments', 'Omnivore', 'Loyal companion animal...'),
('Bear', 'Ursidae', 'Forests and mountains', 'Omnivore', 'Large powerful mammals...'),
('Panda', 'Ailuropoda melanoleuca', 'Chinese bamboo forests', 'Herbivore', 'Black and white bear native to China...'); 