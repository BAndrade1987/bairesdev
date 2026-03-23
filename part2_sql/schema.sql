CREATE TABLE companies (
    companyId INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE users (
    userId INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    city TEXT,
    companyId INTEGER,
    FOREIGN KEY (companyId) REFERENCES companies(companyId)
);

CREATE TABLE posts (
    postId INTEGER PRIMARY KEY,
    userId INTEGER,
    title TEXT,
    body TEXT,
    FOREIGN KEY (userId) REFERENCES users(userId)
);


CREATE INDEX idxUsersCompany ON users(companyId);
CREATE INDEX idxPostsUser ON posts(userId);
CREATE INDEX idxUsersCity ON users(city);

INSERT INTO companies (name)
SELECT DISTINCT company
FROM processedUsersImport;

INSERT INTO users (userId, name, email, city, companyId)
SELECT 
    userId,
    name,
    email,
    city,
    (SELECT companyId FROM companies WHERE name = company)
FROM processedUsersImport;

INSERT INTO posts (postId, userId, title, body)
SELECT id, userId, title, body
FROM postsApiImport;