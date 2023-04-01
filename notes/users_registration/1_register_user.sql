/* Регистрация пользователя
Отправляем POST запрос на http://127.0.0.1:8000/auth/users/
{
    "email": "maximchik.alexandr@yandex.ru",
    "password": "12345qwertyasdfg",
    "re_password": "12345qwertyasdfg"
}

Джнаго проверяет есть ли пользователь с указанным email:  */
SELECT 1 AS "a"
FROM "users_customuser"
WHERE "users_customuser"."email" = 'maximchik.alexandr@yandex.ru'
LIMIT 1;


BEGIN; -- Команда видна только в wireshark

/* Джанго добавляет пользователя в таблицу и возвращает присвоенный id  */
INSERT INTO "users_customuser"
    ("password", "last_login", "email",
     "first_name", "last_name", "phone_number",
     "cashback_point", "is_superuser", "is_staff",
     "is_active", "date_joined")
VALUES ('pbkdf2_sha256$390000$vvm9Tz1bNITtz73DuER75u$R35G9mp2gMLjRf9+3lWPNles99Z1l99lHeL/ZRvPiys=',
        NULL, 'maximchik.alexandr@yandex.ru',
        NULL, NULL, NULL,
        0, false, false,
        false, '2023-04-01T09:43:45.898620+00:00'::timestamptz)
RETURNING "users_customuser"."id";

/* Делаем аккаунт неактивным. Еще раз. Видимо контрольный */
UPDATE "users_customuser"
SET "is_active" = false
WHERE "users_customuser"."id" = 7;


COMMIT; -- Команда видна только в wireshark


/* В ответ приходит json
{
    "email": "maximchik.alexandr@yandex.ru",
    "id": 7
}
и сообщение на почту */

