
"""MigrationForOrderTable Migration."""

from masoniteorm.migrations import Migration


class MigrationForOrderTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("orders") as table:
            table.increments("id")
            table.integer("total_amount")
            table.integer("user_id").unsigned()
            table.foreign("user_id").references("id").on("users")
            table.date("created_at")
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("orders")
