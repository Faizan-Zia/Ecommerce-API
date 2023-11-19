""" User Model """

from masoniteorm.models import Model
from masoniteorm.relationships import has_many


class User(Model):
    """User Model"""
    @has_many("id", "user_id")
    def orders(self):
        from .Order import Order
        return Order

    pass
