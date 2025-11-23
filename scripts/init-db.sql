-- PAV Personalfinder Database Initialization
-- This script is automatically run when the PostgreSQL container starts

-- Enable UUID extension (if needed in future)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Set timezone
SET timezone = 'Europe/Berlin';

-- Create database (if running manually)
-- This is handled by POSTGRES_DB environment variable in Docker

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE pav_personalfinder TO pav_user;

-- The tables are created by SQLAlchemy models in the application
-- This file can be used for additional database setup if needed
