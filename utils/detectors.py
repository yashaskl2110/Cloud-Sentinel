import re

LEAK_PATTERNS = {
    'aws_access_key': re.compile(r'AKIA[0-9A-Z]{16}'),
    'aws_secret_key': re.compile(r'(?i)aws[_-]?secret[_-]?access[_-]?key[^a-z0-9]*[\'"]?([A-Za-z0-9/+=]{40})[\'"]?'),
    'google_api_key': re.compile(r'AIza[0-9A-Za-z-_]{35}'),
    'slack_webhook': re.compile(r'https://hooks\.slack\.com/services/[A-Za-z0-9]+/[A-Za-z0-9]+/[A-Za-z0-9]+'),
    'url_password': re.compile(r'https?:\/\/(?:\w+:\w+@)[^\s/]+'),
    'email_password_combo': re.compile(r'[\w\.-]+@[\w\.-]+\.\w+:[^\s]+'),
    'env_db_password': re.compile(r'(?i)(DB_PASSWORD|DB_PASS|MYSQL_PASSWORD|DATABASE_PASSWORD)[^a-z0-9]*[\'"]?([^\s\'"]+)[\'"]?'),
    'env_secret_key': re.compile(r'(?i)(SECRET_KEY|APP_SECRET|JWT_SECRET)[^a-z0-9]*[\'"]?([^\s\'"]+)[\'"]?'),
    'env_email_pass': re.compile(r'(?i)(EMAIL_PASS|EMAIL_PASSWORD|SMTP_PASS)[^a-z0-9]*[\'"]?([^\s\'"]+)[\'"]?'),
    'env_api_key': re.compile(r'(?i)(API_KEY|APISECRET|APIKEY|APP_KEY)[^a-z0-9]*[\'"]?([^\s\'"]+)[\'"]?')
}

def detect_sensitive_content(content: str, file_path: str):
    leaks = []
    for label, pattern in LEAK_PATTERNS.items():
        matches = pattern.findall(content)
        for match in matches:
            value = match[-1] if isinstance(match, tuple) else match
            leaks.append((file_path, label, value))
    return leaks
