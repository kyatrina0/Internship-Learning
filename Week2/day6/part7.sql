SELECT department, AVG(salary) AS average_salary
FROM employees
GROUP BY department;