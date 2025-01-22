import aiohttp

from app.schemas import ProductSchema


async def get_product(article: str) -> ProductSchema | None:
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={article}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return None
            data = await response.json()
            try:
                product_info = data["data"]["products"][0]
            except KeyError as e:
                return None
            except IndexError as e:
                return None
            data = {
                "article": article,
                "name": product_info["name"],
                "price": product_info["salePriceU"] / 100,
                "rating": product_info.get("reviewRating", 0),
                "stock": product_info.get("totalQuantity", 0)
            }
            return ProductSchema(**data)

