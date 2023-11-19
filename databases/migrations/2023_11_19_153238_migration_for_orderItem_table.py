
"""MigrationForOrderItemTable Migration."""

from masoniteorm.migrations import Migration


class MigrationForOrderItemTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("orderItems") as table:
            table.increments("id")
            table.integer("quantity").unsigned()
            table.integer("product_id").unsigned()
            table.foreign("product_id").references("id").on("products")
            table.integer("order_id").unsigned()
            table.foreign("order_id").references("id").on("orders")
            table.date("created_at")
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("orderItems")
