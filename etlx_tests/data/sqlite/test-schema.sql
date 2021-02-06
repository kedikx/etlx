CREATE TABLE "product" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "name" TEXT NOT NULL,
  "description" TEXT,
  "created" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated" INTEGER NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX "product_idx_created" ON "product" ("created"); 

CREATE TABLE "customer" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "firstName" TEXT NOT NULL,
  "lastName" TEXT NOT NULL,
  "comments" TEXT,
  "created" INTEGER NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated" INTEGER NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX "customer_idx_created" ON "customer" ("created"); 
