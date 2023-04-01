-- Вносим в форму данные заказа и жмем "save"

BEGIN; -- Команда видна только в wireshark

-- Загружаем инфу по выбранному промокоду
SELECT "catalog_promocode"."id",
       "catalog_promocode"."name",
       "catalog_promocode"."percent",
       "catalog_promocode"."date_start",
       "catalog_promocode"."date_end",
       "catalog_promocode"."is_cumulative"
FROM "catalog_promocode"
WHERE "catalog_promocode"."id" = 789 LIMIT 21;

-- Загружаем инфу по выбранному пользователю
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
WHERE "users_customuser"."id" = 10
LIMIT 21;

-- Тут я так понимаю, перепроверяется наличие выбранных
-- каталога и пользователя. Зачем эти запросы, мы же внутри транзакции?
SELECT 1 AS "a"
FROM "catalog_promocode"
WHERE "catalog_promocode"."id" = 789
LIMIT 1;

SELECT 1 AS "a"
FROM "users_customuser"
WHERE "users_customuser"."id" = 10
LIMIT 1;

-- Создаем ордер
INSERT INTO "catalog_order"
    ("date_created", "promocode_id", "delivery_method",
     "delivery_address", "delivery_status", "delivery_notif_in_time",
     "payment_method", "payment_status", "user_id", "result")
VALUES ('2023-04-05T06:00:00+00:00'::timestamptz, 789, 'Post',
        'some addr', 'In process', 24,
        'Card', 'In process', 10, 1202.04)
RETURNING "catalog_order"."id";

SELECT "django_content_type"."id",
       "django_content_type"."app_label",
       "django_content_type"."model"
FROM "django_content_type"
WHERE ("django_content_type"."app_label" = 'catalog'
           AND
       "django_content_type"."model" = 'order')
LIMIT 21;

INSERT INTO "django_admin_log"
    ("action_time", "user_id", "content_type_id",
     "object_id", "object_repr", "action_flag", "change_message")
VALUES ('2023-04-01T12:30:52.077039+00:00'::timestamptz, 5, 15,
        '2', 'Order object (2)', 1, '[{"added": {}}]')
RETURNING "django_admin_log"."id";


COMMIT;  -- Команда видна только в wireshark
