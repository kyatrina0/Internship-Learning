SELECT
    d.manager,
    AVG(e.salary) AS average_salary
FROM departments d
INNER JOIN employees e
ON d.department = e.department
GROUP BY d.manager;