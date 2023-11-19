""" Order Model """

from masoniteorm.models import Model


class Order(Model):
    """Order Model"""
    @has_many("id", "order_id")
    def order_items(self):
        from .OrderItem import OrderItem
        return OrderItem()
