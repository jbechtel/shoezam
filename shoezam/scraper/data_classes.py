import attr
from attr.validators import instance_of, optional
import typing as T


@attr.s
class ProductDetails:
    url: str = attr.ib(validator=instance_of(str))
    sku: int = attr.ib(validator=instance_of(int))
    msrp: float = attr.ib(validator=instance_of(float))
    category: str = attr.ib(validator=instance_of(str))
    subcategory: str = attr.ib(validator=instance_of(str))
    brand: str = attr.ib(validator=instance_of(str))
    name: str = attr.ib(validator=instance_of(str))
    color: str = attr.ib(validator=instance_of(str))
    colorID: int = attr.ib(validator=instance_of(int))
    brandID: int = attr.ib(validator=instance_of(int))
    productID: int = attr.ib(validator=instance_of(int))
    styleID: int = attr.ib(validator=instance_of(int))
    image_urls: T.Dict[str, str] = attr.ib()
    like_product_urls: T.Sequence[str] = attr.ib()
    sale: T.Optional[float] = attr.ib(validator=optional(instance_of(float)),
                                      default=None)

