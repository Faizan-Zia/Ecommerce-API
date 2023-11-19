"""MigrationForProductCategoryTable Migration."""

from masoniteorm.migrations import Migration


class MigrationForProductCategoryTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("productCategories") as table:
            table.increments("id")
            table.string("name").unique()
            table.string("description")
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("productCategories")
