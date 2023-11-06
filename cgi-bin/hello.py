import http.cookies
import os

# Отримання cookies із запиту
comments_cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
comments_count = int(comments_cookie.get("comments_count").value) if "comments_count" in comments_cookie else 0

# Виведення HTML-коду із кількістю коментарів і самими коментарями, а також кнопкою "Видалити cookies"
print("Content-type:text/html\r\n\r\n")
template_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Коментарі</title>
</head>
<body>
    <h1>Кількість коментарів: {comments_count}</h1>
    <h2>Останні коментарі:</h2>
    <pre>
    {open("comments.txt", "r").read()}
    </pre>
    <form action="/cgi-bin/form_handler.py" method="post">
        <input type="submit" name="delete_cookies" value="Видалити cookies">
    </form>
</body>
</html>
"""
print(template_html)

