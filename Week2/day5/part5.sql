SELECT
    e.name AS employee_name,
    d.manager
FROM employees e
INNER JOIN departments d
ON e.department = d.department;