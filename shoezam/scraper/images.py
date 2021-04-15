import typing as T
from pathlib import Path
import attr
import logging
from torpy.http.requests import TorRequests
from shoezam.scraper.data_classes import ProductDetails

logger = logging.getLogger(__name__)

DEFAULT_CONNECTION_REFRESH_RATE = 5


@attr.s(auto_attribs=True)
class Scraper:

    @staticmethod
    def scrape_url(url: str):
        with TorRequests() as tor_requests:
            logger.debug("build circuit")
            with tor_requests.get_session() as sess:
                logger.info(sess.get("http://httpbin.org/ip").json())
                content = sess.get(url).content
                logger.debug(content)
                return content


@attr.s(auto_attribs=True)
class ImageDownloader:
    # refresh_rate: int = DEFAULT_CONNECTION_REFRESH_RATE

    def get_product_images(self, details: ProductDetails) -> T.Dict:
        images = dict()
        for description, url in details.image_urls.items():
            images[description] = Scraper.scrape_url(url)
        return images


@attr.s(auto_attribs=True)
class dataIO:
    source_dir: Path = attr.ib(default=Path('../data/'))

    def __attrs_post_init__(self):
        self.source_dir.mkdir(exist_ok=True)

    @staticmethod
    def product_dir_key(details: ProductDetails) -> str:
        return '_'.join((details.category, 'product', str(details.productID),  'color', str(details.colorID)))

    def product_dir(self, details: ProductDetails) -> Path:
        product_dir = self.source_dir / self.product_dir_key(details)
        product_dir.mkdir(exist_ok=True)
        return product_dir

    def image_path(self, details: ProductDetails, image_key: str) -> Path:
        return self.product_dir(details) / f"{image_key}.jpg"

    def save_images(self, images: T.Dict, details: ProductDetails):
        for desc, image in images.items():
            fout = open(self.image_path(details, desc), "wb")
            logger.info(f'Writing Image {desc}')
            fout.write(image)
            fout.close()










