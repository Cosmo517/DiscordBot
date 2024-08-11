# Imported Modules
from typing import Callable, Coroutine
from functools import wraps
from common.database.database import SessionLocal

# database decorator
def database_connect(func: Callable[..., Coroutine]) -> Callable[..., Coroutine]:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        session = SessionLocal()
        try:
            result = await func(*args, **kwargs, session=session)
            return result
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            session.close()

    return wrapper