-- Create the database
CREATE DATABASE IF NOT EXISTS scia_platform;
USE scia_platform;

-- Courses table
CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2)
);

-- Users table (for example, in case you need user-related data for transactions)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Blogs table
CREATE TABLE IF NOT EXISTS blogs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    published_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Transactions table for storing payment info
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    course_id INT,
    payment_status ENUM('pending', 'completed', 'failed') DEFAULT 'pending',
    transaction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);
-- Insert sample courses into the courses table
INSERT INTO courses (name, description, price) VALUES
('Course 1: Introduction to Python', 'Learn the basics of Python programming.', 29.99),
('Course 2: Web Development with Flask', 'Learn how to build web apps using Flask.', 49.99),
('Course 3: Data Science with Python', 'Explore data analysis and machine learning with Python.', 99.99);


