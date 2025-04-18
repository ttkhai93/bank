import asyncio
from logging import getLogger

from sqlalchemy.exc import DBAPIError


def retry_on_serialization_error(max_retries=3, delay=0.1):
    """
    Recommend: max_retries + 1 >= expected max concurrent requests
    :param max_retries: int
    :param delay: float
    :return:
    """
    logger = getLogger(f"{__name__}.retry_on_serialization_error")

    def decorator(func):
        async def wrapper(*args, **kwargs):
            retries = 0
            while retries <= max_retries:
                try:
                    return await func(*args, **kwargs)
                except DBAPIError as exc:
                    is_serialization_error = "could not serialize access due to concurrent update" in str(exc)
                    if not is_serialization_error:
                        raise

                    if retries == max_retries:
                        logger.debug(f"Reach maximum retries: {max_retries}")
                        raise

                    retries += 1
                    logger.debug(f"Retrying in {delay} seconds...")
                    await asyncio.sleep(delay * (2**retries))
                    logger.warning(f"Retry attempt: {retries}")

        return wrapper

    return decorator


def retry_on_deadlock_error(max_retries=3, delay=0.1):
    """
    Recommend: max_retries + 1 >= expected max concurrent requests
    :param max_retries: int
    :param delay: float
    :return:
    """
    logger = getLogger(f"{__name__}.retry_on_deadlock_error")

    def decorator(func):
        async def wrapper(*args, **kwargs):
            retries = 0
            while retries <= max_retries:
                try:
                    return await func(*args, **kwargs)
                except DBAPIError as exc:
                    is_deadlock_error = "deadlock detected" in str(exc)
                    if not is_deadlock_error:
                        raise

                    if retries == max_retries:
                        logger.debug(f"Reach maximum retries: {max_retries}")
                        raise

                    retries += 1
                    logger.debug(f"Retrying in {delay} seconds...")
                    await asyncio.sleep(delay * (2**retries))
                    logger.warning(f"Retry attempt: {retries}")

        return wrapper

    return decorator


def retry_on_version_conflict_error(max_retries=3, delay=0.1):
    """
    Recommend: max_retries + 1 >= expected max concurrent requests
    :param max_retries: int
    :param delay: float
    :return:
    """
    logger = getLogger(f"{__name__}.retry_on_version_conflict_error")

    def decorator(func):
        async def wrapper(*args, **kwargs):
            retries = 0
            while retries <= max_retries:
                try:
                    return await func(*args, **kwargs)
                except ValueError as exc:
                    is_version_conflict_error = "Version conflict" in str(exc)
                    if not is_version_conflict_error:
                        raise

                    if retries == max_retries:
                        logger.debug(f"Reach maximum retries: {max_retries}")
                        raise

                    retries += 1
                    logger.debug(f"Retrying in {delay} seconds...")
                    await asyncio.sleep(delay * (2**retries))
                    logger.warning(f"Retry attempt: {retries}")

        return wrapper

    return decorator
