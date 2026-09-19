SELECT
    departments.department,
    departments.manager,
    employees.name
FROM employees
RIGHT JOIN departments
ON employees.department = departments.department;