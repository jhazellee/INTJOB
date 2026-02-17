
SELECT * FROM users; -- To verify the table creation

/* SQL script to create Job Posting table */
CREATE TABLE jobs (
    jobID INT PRIMARY KEY IDENTITY(1,1),
    employer_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(MAX) NOT NULL,
    company VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    salary INT NOT NULL,
    status VARCHAR(50) DEFAULT 'Active',
    created_at DATETIME DEFAULT GETDATE()
);

SELECT * FROM jobs; -- To verify the table creation

-- The Skill Library (Stores the name of the skill)
CREATE TABLE skills (
    id INT IDENTITY(1,1) PRIMARY KEY,
    skill_name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50) -- e.g., 'Technical', 'Soft', 'WebDev-Sub'
);

INSERT INTO skills (skill_name, category) VALUES 
('Graphic Design', 'Technical'),
('Web Development', 'Technical'),
('Frontend', 'WebDev-Sub'),
('Statistics', 'DataAnalysis-Sub'),
('Teamwork', 'Soft');

SELECT * FROM skills; -- To verify the table creation and data insertion

-- User_Skills Junction Table (Links Users to Skills)
CREATE TABLE user_skills (
    user_id INT NOT NULL,
    skill_id INT NOT NULL,
    PRIMARY KEY (user_id, skill_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
);

SELECT * FROM user_skills; -- To verify the table creation

SELECT u.full_name, s.skill_name 
FROM users u 
JOIN user_skills us ON u.id = us.user_id 
JOIN skills s ON us.skill_id = s.id; -- To verify the relationships and data retrieval
