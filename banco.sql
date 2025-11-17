-- Criar schemas separados
CREATE SCHEMA IF NOT EXISTS flask_schema;
CREATE SCHEMA IF NOT EXISTS laravel_schema;

-- Criar tabela users no schema do Flask
CREATE TABLE IF NOT EXISTS flask_schema.users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    username VARCHAR(80) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Criar tabela users no schema do Laravel
CREATE TABLE IF NOT EXISTS laravel_schema.users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    username VARCHAR(80) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
