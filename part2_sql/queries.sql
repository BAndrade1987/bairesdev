SELECT c.name AS company, COUNT(p.postId) AS totalPosts
FROM companies c
JOIN users u ON u.companyId = c.companyId
JOIN posts p ON p.userId = u.userId
GROUP BY c.name
ORDER BY totalPosts DESC
LIMIT 5;

SELECT city, COUNT(*) AS totalUsers
FROM users
GROUP BY city
ORDER BY totalUsers DESC;

SELECT
    c.name AS company,
    AVG(userPostCount) AS avgPostsPerUser
FROM (
    SELECT u.userId, u.companyId, COUNT(p.postId) AS userPostCount
    FROM users u
    LEFT JOIN posts p ON p.userId = u.userId
    GROUP BY u.userId
) t
JOIN companies c ON c.companyId = t.companyId
GROUP BY c.name;