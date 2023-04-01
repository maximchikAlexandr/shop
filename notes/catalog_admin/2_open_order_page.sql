-- Переходим на лист с ордерами: http://127.0.0.1:8000/admin/catalog/order/.

-- Количество строк в таблице "catalog_order"
SELECT COUNT(*) AS "__count" FROM "catalog_order";

-- Загружаем все ордера с их покупателями
SELECT "catalog_order"."id",
       "catalog_order"."date_created",
       "catalog_order"."promocode_id",
       "catalog_order"."delivery_method",
       "catalog_order"."delivery_address",
       "catalog_order"."delivery_status",
       "catalog_order"."delivery_notif_in_time",
       "catalog_order"."payment_method",
       "catalog_order"."payment_status",
       "catalog_order"."user_id",
       "catalog_order"."result",
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
       "users_customuser"."date_joined"
FROM "catalog_order"
    LEFT OUTER JOIN "users_customuser"
        ON ("catalog_order"."user_id" = "users_customuser"."id")
ORDER BY "catalog_order"."id"
DESC;
