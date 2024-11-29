CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

INSERT INTO users (name, email) VALUES
('Alice123', 'alice@example.com'),
('Bob234', 'bob@example.com'),
('Charlie345', 'charlie@example.com')
ON CONFLICT DO NOTHING;
