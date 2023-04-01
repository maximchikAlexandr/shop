-- Жмем "add order" - переходим на http://127.0.0.1:8000/admin/catalog/order/add/

SELECT "django_content_type"."id",
       "django_content_type"."app_label",
       "django_content_type"."model"
FROM "django_content_type"
WHERE
    ("django_content_type"."app_label" = 'catalog'
         AND
     "django_content_type"."model" = 'order')
LIMIT 21;

-- создаются три курсора
DECLARE "_django_curs_140190493435456_sync_1"
    NO SCROLL CURSOR WITH HOLD FOR
    SELECT "catalog_promocode"."id",
           "catalog_promocode"."name",
           "catalog_promocode"."percent",
           "catalog_promocode"."date_start",
           "catalog_promocode"."date_end",
           "catalog_promocode"."is_cumulative"
    FROM "catalog_promocode";

DECLARE "_django_curs_140190493435456_sync_2" NO SCROLL CURSOR WITH HOLD FOR
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
    ORDER BY "users_customuser"."email"
    ASC;

DECLARE "_django_curs_140190493435456_sync_3" NO SCROLL CURSOR WITH HOLD FOR
    SELECT "catalog_product"."id",
           "catalog_product"."name",
           "catalog_product"."price",
           "catalog_product"."count_on_stock",
           "catalog_product"."articul",
           "catalog_product"."description",
           "catalog_product"."discount_id",
           "catalog_product"."category_id",
           "catalog_product"."producer_id"
    FROM "catalog_product";

-- У меня в базе 2000 товаров, созданных с помощью faker
-- Джанго выполняет 2000 таких запросов к БД (см. файл logs)
SELECT "catalog_category"."id",
       "catalog_category"."name",
       "catalog_category"."description"
FROM "catalog_category"
WHERE "catalog_category"."id" = 379
LIMIT 21;
