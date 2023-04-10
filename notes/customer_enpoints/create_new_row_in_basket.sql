-- Получаем пользователя
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


SELECT "catalog_product"."id",
       "catalog_product"."name",
       "catalog_product"."price",
       "catalog_product"."count_on_stock",
       "catalog_product"."articul",
       "catalog_product"."description",
       "catalog_product"."discount_id",
       "catalog_product"."category_id",
       "catalog_product"."producer_id"
FROM "catalog_product"
WHERE "catalog_product"."id" = 540
LIMIT 21;

SELECT "catalog_basket"."id",
       "catalog_basket"."user_id",
       "catalog_basket"."product_id",
       "catalog_basket"."count"
FROM "catalog_basket"
WHERE
    ("catalog_basket"."product_id" = 540
         AND
     "catalog_basket"."user_id" = 10)
LIMIT 21;

-- Вставка новой записи в корзину
BEGIN;

INSERT INTO "catalog_basket" ("user_id", "product_id", "count")
VALUES (10, 540, NULL)
RETURNING "catalog_basket"."id";

COMMIT;

UPDATE "catalog_basket"
SET "user_id" = 10,
    "product_id" = 540,
    "count" = 1
WHERE "catalog_basket"."id" = 7;

