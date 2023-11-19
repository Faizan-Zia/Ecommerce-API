""" Product Model """

from masoniteorm.models import Model
from masoniteorm.relationships import belongs_to

class Product(Model):
    """Product Model"""

    @belongs_to('category_id', 'id')
    def category(self):
        from models.ProductCategory import ProductCategory
        return ProductCategory
