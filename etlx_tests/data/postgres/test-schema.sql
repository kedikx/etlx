DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS customer;

CREATE OR REPLACE FUNCTION set_updated() 
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated = timezone('utc', now()); RETURN NEW; END; $$ language 'plpgsql';

CREATE TABLE "product" (
  "id" SERIAL NOT NULL PRIMARY KEY,
  "name" VARCHAR(45) NOT NULL UNIQUE,
  "description" TEXT,
  "created" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated" TIMESTAMP NOT NULL DEFAULT timezone('utc', now())
);

CREATE INDEX "product_idx_created" ON "product" ("created");

DROP TRIGGER IF EXISTS set_updated ON "product";
CREATE TRIGGER set_updated BEFORE UPDATE ON "product" FOR EACH ROW EXECUTE PROCEDURE set_updated();


CREATE TABLE "customer" (
  "id" SERIAL NOT NULL,
  "firstName" VARCHAR(45) NOT NULL,
  "lastName" VARCHAR(45) NOT NULL,
  "comments" TEXT,
  "created" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated" TIMESTAMP NOT NULL DEFAULT timezone('utc', now()),
  CONSTRAINT "customer_pk" PRIMARY KEY ("id")
);

CREATE INDEX "customer_idx_created" ON "customer" ("created");

DROP TRIGGER IF EXISTS set_updated ON "customer";
CREATE TRIGGER set_updated BEFORE UPDATE ON "customer" FOR EACH ROW EXECUTE PROCEDURE set_updated();
