from typing import Annotated

from fastapi import Depends
from fastapi_limiter.depends import RateLimiter


RateLimiter3PerSecond = Annotated[None, Depends(RateLimiter(times=3, seconds=1))]
