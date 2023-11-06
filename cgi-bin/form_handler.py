import cgi
import html
import http.cookies
import os
import datetime  # Для встановлення часу життя cookie

# Отримання даних з форми
form = cgi.FieldStorage()

# Отримання ім'я користувача та коментаря з форми
username = form.getfirst("username", "Анонім")
comment = form.getfirst("comment", "")
username = html.escape(username)
comment = html.escape(comment)

# Обробка вибору мови
lang = form.getvalue("lang", "не обрано мову")

# Перевірка, чи користувач ввійшов в систему
is_authenticated = False
if "username" in os.environ and "password" in os.environ:
    is_authenticated = True

# Встановлення cookies для імітації автентифікації
if is_authenticated:
    username = os.environ.get("username")
    password = os.environ.get("password")
else:
    username = "Гість"

# Збереження коментарів у текстовому файлі
with open("comments.txt", "a") as file:
    file.write(f"Користувач: {username}\nКоментар: {comment}\n\n")

# Отримання cookies з запиту
cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
comments_count = int(cookie.get("comments_count").value) if "comments_count" in cookie else 0

# Обробка кнопки "Видалити cookies"
delete_cookies = form.getfirst("delete_cookies", "")

if delete_cookies:
    # Встановлення cookie з видаленням шляхом встановлення часу життя в минуле
    expired_time = datetime.datetime(1970, 1, 1)
    delete_cookie = http.cookies.SimpleCookie()
    delete_cookie["username"] = ""
    delete_cookie["username"]["expires"] = expired_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
    delete_cookie["password"] = ""
    delete_cookie["password"]["expires"] = expired_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
    delete_cookie["comments_count"] = ""
    delete_cookie["comments_count"]["expires"] = expired_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    # Виведення cookies для видалення
    print(delete_cookie.output())
    
# Отримання cookies з запиту
cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
username_cookie = cookie.get("username").value if "username" in cookie else ""
password_cookie = cookie.get("password").value if "password" in cookie else ""
comments_count = int(cookie.get("comments_count").value) if "comments_count" in cookie else 0

# Обробка кнопки "Видалити cookies"
delete_cookies = form.getfirst("delete_cookies", "")

if delete_cookies:
    # Встановлення cookie з видаленням шляхом встановлення часу життя в минуле
    expired_time = datetime.datetime(1970, 1, 1)
    delete_cookie = http.cookies.SimpleCookie()
    delete_cookie["username"] = ""
    delete_cookie["username"]["expires"] = expired_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
    delete_cookie["password"] = ""
    delete_cookie["password"]["expires"] = expired_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
    delete_cookie["comments_count"] = ""
    delete_cookie["comments_count"]["expires"] = expired_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    # Виведення cookies для видалення
    print(delete_cookie.output())
else:
    # Збільшення лічильника коментарів
    comments_count += 1
    # Оновлення cookie з лічильником коментарів
    cookie["comments_count"] = comments_count

    # Виведення cookies з оновленою кількістю коментарів
    print(cookie.output())
    
# Виведення HTML-коду
print("Content-type:text/html\r\n\r\n")
template_html = f"""
<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Форма коментарів</title>
</head>
<body>
    <h1>Ласкаво просимо, {username}!</h1>
    <form action="/cgi-bin/form_handler.py" method="post">
        Ваше ім'я: <input type="text" name="username" value="{username_cookie}">
        <br>
        Коментар:
        <br>
        <textarea name="comment" rows="4" cols="50">{comment}</textarea>
        <br>
        <input type="radio" name="lang" value="en"> Англійська
        <input type="radio" name="lang" value="ua"> Українська
        <br>
        <input type="submit" value="Відправити коментар">
    </form>
    <h2>Ваш коментар:</h2>
    <p>{comment}</p>
</body>
</html>
"""
print(template_html)



