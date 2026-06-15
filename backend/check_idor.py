with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all endpoints and check if they verify ownership
import re
endpoints = re.findall(r'@app\.(get|post|patch|delete)\("([^"]+)"', content)
for method, path in endpoints:
    print(f"{method.upper():6} {path}")