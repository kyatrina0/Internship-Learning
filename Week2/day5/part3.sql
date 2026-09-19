SELECT
    employees.name,
    employees.department,
    departments.manager
FROM employees
LEFT JOIN departments
ON employees.department = departments.department;