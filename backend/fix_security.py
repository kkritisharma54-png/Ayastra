with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'SECRET_KEY = "ayastra-secret-key"',
    'SECRET_KEY = os.getenv("SECRET_KEY", "fallback-change-in-production")'
)
content = content.replace(
    '"ayastra-secret-key"',
    'os.getenv("SECRET_KEY", "fallback-change-in-production")'
)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")