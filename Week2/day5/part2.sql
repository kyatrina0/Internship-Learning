SELECT
    employees.name,
    employees.department,
    departments.manager
FROM employees
INNER JOIN departments
ON employees.department = departments.department;