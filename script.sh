masonite-orm model User --directory models
masonite-orm model Product --directory models
# masonite-orm model Inventory --directory models
masonite-orm model Order --directory models
masonite-orm model OrderItem --directory models
masonite-orm model ProductCategory --directory models

masonite-orm migration migration_for_user_table --create users
masonite-orm migration migration_for_productCategory_table --create productCategories
masonite-orm migration migration_for_product_table --create products
# masonite-orm migration migration_for_inventory_table --create inventories
masonite-orm migration migration_for_orderItem_table --create orderItems
masonite-orm migration migration_for_order_table --create orders

masonite-orm migrate
masonite-orm migrate:refresh

service postgresql start
export SECRET_KEY="StrongSecretKey"
uvicorn main:app --host=0.0.0.0 --port=8000 --reload