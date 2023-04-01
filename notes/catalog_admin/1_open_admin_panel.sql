-- Загружаем админку http://127.0.0.1:8000/admin/

-- аутентификация
SELECT "django_session"."session_key",
       "django_session"."session_data",
       "django_session"."expire_date"
FROM "django_session"
WHERE
    ("django_session"."expire_date" > '2023-04-01T11:27:06.225254+00:00'::timestamptz
         AND
     "django_session"."session_key" = '9p6ganx7lr3ksfdq71hcr4lvdawul28l')
LIMIT 21;

-- загружаем инфу по админу
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
WHERE "users_customuser"."id" = 5
LIMIT 21;

-- Запрос для таблицы "Recent actions" на странице http://127.0.0.1:8000/admin/
SELECT "django_admin_log"."id",
       "django_admin_log"."action_time",
       "django_admin_log"."user_id",
       "django_admin_log"."content_type_id",
       "django_admin_log"."object_id",
       "django_admin_log"."object_repr",
       "django_admin_log"."action_flag",
       "django_admin_log"."change_message",
       "users_customuser"."id",
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
       "users_customuser"."date_joined",
       "django_content_type"."id",
       "django_content_type"."app_label",
       "django_content_type"."model"
FROM "django_admin_log"
    INNER JOIN "users_customuser"
        ON ("django_admin_log"."user_id" = "users_customuser"."id")
    LEFT OUTER JOIN "django_content_type"
        ON ("django_admin_log"."content_type_id" = "django_content_type"."id")
WHERE "django_admin_log"."user_id" = 5
ORDER BY "django_admin_log"."action_time"
DESC LIMIT 10;
