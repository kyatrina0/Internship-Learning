SELECT
    d.manager,
    COUNT(e.id) AS employee_count
FROM departments d
LEFT JOIN employees e
ON d.department = e.department
GROUP BY d.manager;