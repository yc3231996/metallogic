
from sqlglot import parse, transpile, dialects


sql = """SELECT DATE_FORMAT(transactiondate, '%Y-%m') AS month, SUM(netamount) AS monthly_sales
FROM saleswidetable
WHERE transactiondate >= DATE_SUB('2024-07-22', INTERVAL 1 YEAR)
GROUP BY month
ORDER BY month;"""


parsed = parse(sql)
print("Parsed SQL:", parsed)

# 使用 transpile 函数
postgres_sql = transpile(sql, write='postgres')[0]
print("postgres:", postgres_sql)
