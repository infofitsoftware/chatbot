-- Database setup script for Chat Application
-- This script creates the necessary database and tables

-- Create database (run this as a superuser)
-- CREATE DATABASE chatbot_db;

-- Connect to the chatbot_db database
-- \c chatbot_db;

-- Create the messages table
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create an index on timestamp for better query performance
CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp);

-- Create an index on id for better query performance
CREATE INDEX IF NOT EXISTS idx_messages_id ON messages(id);

-- Insert some sample data (optional)
INSERT INTO messages (user_message, ai_response) VALUES 
('Hello, how are you?', 'Hello! I am doing well, thank you for asking. How can I help you today?'),
('What is artificial intelligence?', 'Artificial Intelligence (AI) is a branch of computer science that aims to create machines and software that can perform tasks that typically require human intelligence. This includes learning, reasoning, problem-solving, perception, and language understanding.'),
('Tell me a joke', 'Why don''t scientists trust atoms? Because they make up everything! 😄');

-- Grant permissions (adjust username as needed)
-- GRANT ALL PRIVILEGES ON DATABASE chatbot_db TO your_username;
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_username;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_username;

-- Show table structure
\d messages;

-- Show sample data
SELECT * FROM messages ORDER BY timestamp DESC LIMIT 5;
