CREATE DATABASE "test_shop_db";

SET TIME ZONE 'UTC';

-- Запрос № 3. Повторяется 3 раза
EXPLAIN ANALYZE
SELECT
    c.relname,
    CASE
        WHEN c.relispartition THEN 'p'
        WHEN c.relkind IN ('m', 'v') THEN 'v'
        ELSE 't'
    END
FROM pg_catalog.pg_class c
LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
WHERE c.relkind IN ('f', 'm', 'p', 'r', 'v')
    AND n.nspname NOT IN ('pg_catalog', 'pg_toast')
    AND pg_catalog.pg_table_is_visible(c.oid);

BEGIN;
-- создаются все таблицы "из коробки" джанго и пользовательские таблицы
-- создаются констрейты (FOREIGN KEY, UNIQUE) между таблицами и индексы по столбцам с id, key,
-- email, date
CREATE INDEX "auth_group_name_a6ea08ec_like" ON "auth_group" ("name" varchar_pattern_ops);

-- varchar_pattern_ops - поддерживает индексы-B-деревья для типа varchar
COMMIT;
-- Запрос № 3.

SELECT "django_content_type"."id",
       "django_content_type"."app_label",
       "django_content_type"."model"
FROM "django_content_type"
WHERE "django_content_type"."app_label" = 'admin';

-- Далее внутри конструкций BEGIN ... COMMIT вставляются данные в таблицы джанго и
-- пользовательские таблицы. В последние - каждая строчка вставляется отдельно.

-- Строки вставляются так. Сначало джанго пытается обновить строку с несуществующими id
UPDATE "catalog_promocode"
SET "name" = 'PYFYGBD3',
    "percent" = 45,
    "date_start" = '2023-03-19'::date,
    "date_end" = '2023-04-19'::date,
    "is_cumulative" = true
WHERE "catalog_promocode"."id" = 996;
-- На что получает от БД: UPDATE 0
-- И только потом происходит инсрерт
INSERT INTO "catalog_promocode" ("id", "name", "percent", "date_start", "date_end", "is_cumulative")
VALUES (996, 'PYFYGBD3', 45, '2023-03-19'::date, '2023-04-19'::date, true)
RETURNING "catalog_promocode"."id";

SET CONSTRAINTS ALL IMMEDIATE;

SET CONSTRAINTS ALL DEFERRED;

-- Для всех пользовательских таблиц используются такие запросы
SELECT setval(
    pg_get_serial_sequence('"catalog_discount"','id'),
    coalesce(max("id"), 1),
    max("id") IS NOT null
    )
FROM "catalog_discount";


RELEASE SAVEPOINT "s140005005358912_x1";
SAVEPOINT "s140005005358912_x2";

SELECT "catalog_category"."id",
       "catalog_category"."name",
       "catalog_category"."description"
FROM "catalog_category"
ORDER BY "catalog_category"."id" ASC;


SELECT 1;
SET CONSTRAINTS ALL IMMEDIATE;
SET CONSTRAINTS ALL DEFERRED;

ROLLBACK TO SAVEPOINT "s140005005358912_x2";
RELEASE SAVEPOINT "s140005005358912_x2";
SAVEPOINT "s140005005358912_x3";

SELECT "catalog_discount"."id",
       "catalog_discount"."percent",
       "catalog_discount"."name",
       "catalog_discount"."date_start",
       "catalog_discount"."date_end"
FROM "catalog_discount"
ORDER BY "catalog_discount"."id" ASC;

SELECT 1;
SET CONSTRAINTS ALL IMMEDIATE;
SET CONSTRAINTS ALL DEFERRED;

ROLLBACK TO SAVEPOINT "s140005005358912_x3";
RELEASE SAVEPOINT "s140005005358912_x3";
SAVEPOINT "s140005005358912_x4";



SELECT "catalog_producer"."id",
       "catalog_producer"."name",
       "catalog_producer"."description",
       "catalog_producer"."country"
FROM "catalog_producer"
ORDER BY "catalog_producer"."id" ASC;

SELECT 1;
SET CONSTRAINTS ALL IMMEDIATE;
SET CONSTRAINTS ALL DEFERRED;

ROLLBACK TO SAVEPOINT "s140005005358912_x4";
RELEASE SAVEPOINT "s140005005358912_x4";

ROLLBACK;

SET TIME ZONE 'UTC';

DROP DATABASE "test_shop_db";


