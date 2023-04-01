/* Переходим по ссылке из сообщения, прешедшего на почту.

Далее джанго загружает все поля пользотеля, чтобы поменять одно ("is_active").
   Вопрос: это в джанго везде так или у меня что-то настроено не оптимально?
*/
SELECT "users_customuser"."id",
       "users_customuser"."password",
       "users_customuser"."last_login",
       "users_customuser"."email",
       "users_customuser"."first_name",
       "users_customuser"."last_name",
       "users_customuser"."phone_number",
       "users_customuser"."cashback_point",
       "users_customuser"."is_superuser",
       "users_customuser"."is_staff",
       "users_customuser"."is_active",
       "users_customuser"."date_joined"
FROM "users_customuser"
WHERE "users_customuser"."id" = 7
LIMIT 21;

UPDATE "users_customuser"
SET "password" = 'pbkdf2_sha256$390000$vvm9Tz1bNITtz73DuER75u$R35G9mp2gMLjRf9+3lWPNles99Z1l99lHeL/ZRvPiys=',
    "last_login" = NULL,
    "email" = 'maximchik.alexandr@yandex.ru',
    "first_name" = NULL,
    "last_name" = NULL,
    "phone_number" = NULL,
    "cashback_point" = 0,
    "is_superuser" = false,
    "is_staff" = false,
    "is_active" = true,
    "date_joined" = '2023-04-01T09:43:45.898620+00:00'::timestamptz
WHERE "users_customuser"."id" = 7;
