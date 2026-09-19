SELECT
    d.manager,
    e.name AS employee_name
FROM departments d
INNER JOIN employees e
ON d.department = e.department;