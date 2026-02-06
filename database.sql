
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

