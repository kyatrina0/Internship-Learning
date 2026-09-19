SELECT department, MAX(salary) AS highest_salary
FROM employees
GROUP BY department;