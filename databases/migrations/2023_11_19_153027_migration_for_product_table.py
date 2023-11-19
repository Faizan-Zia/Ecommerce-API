
"""MigrationForProductTable Migration."""

from masoniteorm.migrations import Migration


class MigrationForProductTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("products") as table:
            table.increments("id")
            table.string("name")
            table.string("description")
            table.integer("price")
            table.integer("quantity")
            table.integer("threshold")
            table.integer("category_id").unsigned()
            table.foreign("category_id").references("id").on("productCategories")
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("products")