"""MigrationForUserTable Migration."""

from masoniteorm.migrations import Migration


class MigrationForUserTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("users") as table:
            table.increments("id")
            table.string("username").unique()
            table.string("email").unique()
            table.string("hashed_password")
            table.string("phone_number", 11).nullable()
            table.text("address")

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("users")
