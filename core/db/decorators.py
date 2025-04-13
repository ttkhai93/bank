import asyncio
from logging import getLogger

import sqlalchemy

logger = getLogger(__name__)


def retry_on_serialization_error(max_retries=3, delay=0.1):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            retries = 1
            while retries <= max_retries:
                logger.debug(f"Retry attempt: {retries}")
                try:
                    return await func(*args, **kwargs)
                except sqlalchemy.exc.DBAPIError as exc:
                    is_serialization_error = "could not serialize access due to concurrent update" in str(exc)
                    if not is_serialization_error:
                        raise

                    if retries == max_retries:
                        logger.debug(f"Reach maximum retries: {max_retries}")
                        raise

                    retries += 1
                    logger.debug(f"Retrying in {delay} seconds...")
                    await asyncio.sleep(delay * (2**retries))

        return wrapper

    return decorator
