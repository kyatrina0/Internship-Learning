SELECT
    e.name,
    e.salary,
    d.manager
FROM employees e
INNER JOIN departments d
ON e.department = d.department
WHERE e.department = 'IT';