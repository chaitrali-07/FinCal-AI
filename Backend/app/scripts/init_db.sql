-- Finance & AI Calculator Platform Database Initialization
-- This script creates all necessary tables for the backend

-- Users table
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);


-- Calculation History table
CREATE TABLE IF NOT EXISTS calculation_history (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255),
    calculator_type VARCHAR(50) NOT NULL,
    calculator_name VARCHAR(100),
    calculator_version VARCHAR(10) DEFAULT '1.0',
    inputs JSONB,
    result JSONB,
    formula TEXT,
    assumptions JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_calc_history_user ON calculation_history(user_id);
CREATE INDEX IF NOT EXISTS idx_calc_history_type ON calculation_history(calculator_type);
CREATE INDEX IF NOT EXISTS idx_calc_history_created ON calculation_history(created_at);


-- Calculation Templates table
CREATE TABLE IF NOT EXISTS calculation_templates (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    template_name VARCHAR(255),
    calculator_type VARCHAR(50),
    template_inputs JSONB,
    description TEXT,
    is_favorite INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_templates_user ON calculation_templates(user_id);
CREATE INDEX IF NOT EXISTS idx_templates_type ON calculation_templates(calculator_type);
CREATE INDEX IF NOT EXISTS idx_templates_created ON calculation_templates(created_at);


-- Quick Notes table
CREATE TABLE IF NOT EXISTS quick_notes (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    calculation_history_id INTEGER,
    note_text TEXT,
    tags VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_notes_user ON quick_notes(user_id);
CREATE INDEX IF NOT EXISTS idx_notes_created ON quick_notes(created_at);


-- Add foreign key constraints (optional, depending on your DB setup)
-- ALTER TABLE calculation_history ADD CONSTRAINT fk_calc_history_user FOREIGN KEY (user_id) REFERENCES users(user_id);
-- ALTER TABLE calculation_templates ADD CONSTRAINT fk_templates_user FOREIGN KEY (user_id) REFERENCES users(user_id);
-- ALTER TABLE quick_notes ADD CONSTRAINT fk_notes_user FOREIGN KEY (user_id) REFERENCES users(user_id);
