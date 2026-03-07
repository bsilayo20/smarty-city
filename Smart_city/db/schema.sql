-- PostgreSQL schema for Arusha Smart City Data Link System

CREATE TABLE districts (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  code VARCHAR(10) NOT NULL UNIQUE,
  region TEXT NOT NULL DEFAULT 'Arusha',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE education_centers (
  id SERIAL PRIMARY KEY,
  district_id INTEGER NOT NULL REFERENCES districts(id),
  ward TEXT NOT NULL,
  name TEXT NOT NULL,
  latitude NUMERIC(9,6),
  longitude NUMERIC(9,6),
  student_capacity INTEGER,
  teachers INTEGER,
  student_teacher_ratio NUMERIC(5,2),
  ownership TEXT,
  level TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE facilities_health (
  id SERIAL PRIMARY KEY,
  district_id INTEGER NOT NULL REFERENCES districts(id),
  ward TEXT NOT NULL,
  name TEXT NOT NULL,
  latitude NUMERIC(9,6),
  longitude NUMERIC(9,6),
  bed_capacity INTEGER,
  facility_level TEXT,
  ownership TEXT,
  specialized_services TEXT[],
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE population_stats (
  id SERIAL PRIMARY KEY,
  district_id INTEGER NOT NULL REFERENCES districts(id),
  ward TEXT NOT NULL,
  year INTEGER NOT NULL,
  population INTEGER NOT NULL,
  area_km2 NUMERIC(10,2),
  density_per_km2 NUMERIC(10,2),
  annual_growth_rate NUMERIC(5,4),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE weather_logs (
  id SERIAL PRIMARY KEY,
  district_id INTEGER NOT NULL REFERENCES districts(id),
  ward TEXT NOT NULL,
  observed_at TIMESTAMP WITH TIME ZONE NOT NULL,
  temperature_c NUMERIC(4,1),
  rain_mm NUMERIC(5,2),
  humidity_pct NUMERIC(5,2),
  condition TEXT,
  source TEXT DEFAULT 'synthetic',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE ai_reasoning_logs (
  id SERIAL PRIMARY KEY,
  query_text TEXT NOT NULL,
  response_text TEXT NOT NULL,
  reasoning_steps TEXT[],
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Sample seed data

INSERT INTO districts (name, code, region)
VALUES
  ('Arusha City', 'ARU', 'Arusha'),
  ('Meru', 'MER', 'Arusha'),
  ('Karatu', 'KAR', 'Arusha'),
  ('Monduli', 'MON', 'Arusha');

INSERT INTO education_centers
  (district_id, ward, name, latitude, longitude,
   student_capacity, teachers, student_teacher_ratio, ownership, level)
VALUES
  ((SELECT id FROM districts WHERE code = 'ARU'),
   'Sokon I', 'Arusha Secondary School', -3.369500, 36.686400,
   1200, 60, 20.00, 'Public', 'Secondary'),
  ((SELECT id FROM districts WHERE code = 'ARU'),
   'Sokon I', 'Sakon I Primary School', -3.366000, 36.689000,
   900, 35, 25.71, 'Public', 'Primary'),
  ((SELECT id FROM districts WHERE code = 'MER'),
   'Usa River', 'Usa River Secondary School', -3.365000, 36.853000,
   800, 32, 25.00, 'Public', 'Secondary'),
  ((SELECT id FROM districts WHERE code = 'KAR'),
   'Karatu', 'Karatu High School', -3.335000, 35.670000,
   1000, 38, 26.32, 'Public', 'Secondary'),
  ((SELECT id FROM districts WHERE code = 'MON'),
   'Mto wa Mbu', 'Mto wa Mbu Primary School', -3.366700, 35.850000,
   700, 24, 29.17, 'Public', 'Primary');

INSERT INTO facilities_health
  (district_id, ward, name, latitude, longitude,
   bed_capacity, facility_level, ownership, specialized_services)
VALUES
  ((SELECT id FROM districts WHERE code = 'ARU'),
   'Sekei', 'Mount Meru Regional Hospital', -3.369600, 36.696000,
   450, 'Hospital', 'Public',
   ARRAY['Emergency','Maternal Health','Pediatrics','Surgery','Infectious Diseases']),
  ((SELECT id FROM districts WHERE code = 'MER'),
   'Usa River', 'Meru District Hospital', -3.365500, 36.855500,
   180, 'Hospital', 'Public',
   ARRAY['Maternal Health','Outpatient','HIV Care']),
  ((SELECT id FROM districts WHERE code = 'KAR'),
   'Karatu', 'Karatu District Hospital', -3.334000, 35.668000,
   210, 'Hospital', 'Public',
   ARRAY['Emergency','Maternal Health','Malaria Treatment']),
  ((SELECT id FROM districts WHERE code = 'MON'),
   'Monduli Juu', 'Monduli District Hospital', -3.300000, 36.450000,
   160, 'Hospital', 'Public',
   ARRAY['Outpatient','Maternal Health','Community Health Outreach']);

INSERT INTO population_stats
  (district_id, ward, year, population, area_km2,
   density_per_km2, annual_growth_rate)
VALUES
  ((SELECT id FROM districts WHERE code = 'ARU'),
   'Sokon I', 2025, 32000, 12.50, 2560, 0.0350),
  ((SELECT id FROM districts WHERE code = 'ARU'),
   'Sekei', 2025, 28000, 10.20, 2745, 0.0320),
  ((SELECT id FROM districts WHERE code = 'MER'),
   'Usa River', 2025, 26000, 40.00, 650, 0.0380),
  ((SELECT id FROM districts WHERE code = 'KAR'),
   'Karatu', 2025, 21000, 35.00, 600, 0.0410),
  ((SELECT id FROM districts WHERE code = 'MON'),
   'Monduli Juu', 2025, 17000, 50.00, 340, 0.0290),
  ((SELECT id FROM districts WHERE code = 'MON'),
   'Mto wa Mbu', 2025, 23000, 30.00, 767, 0.0430);

INSERT INTO weather_logs
  (district_id, ward, observed_at, temperature_c, rain_mm,
   humidity_pct, condition, source)
VALUES
  ((SELECT id FROM districts WHERE code = 'ARU'),
   'Sekei', '2026-03-07T09:00:00Z', 21.5, 3.2, 76.0, 'light rain', 'synthetic'),
  ((SELECT id FROM districts WHERE code = 'ARU'),
   'Sokon I', '2026-03-07T09:00:00Z', 22.0, 2.5, 74.0, 'cloudy', 'synthetic'),
  ((SELECT id FROM districts WHERE code = 'MER'),
   'Usa River', '2026-03-07T09:00:00Z', 20.0, 5.5, 82.0, 'moderate rain', 'synthetic'),
  ((SELECT id FROM districts WHERE code = 'KAR'),
   'Karatu', '2026-03-07T09:00:00Z', 18.5, 7.0, 88.0, 'heavy rain', 'synthetic'),
  ((SELECT id FROM districts WHERE code = 'MON'),
   'Mto wa Mbu', '2026-03-07T09:00:00Z', 23.0, 6.0, 85.0, 'moderate rain', 'synthetic');

