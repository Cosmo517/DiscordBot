# Imported Modules
from typing import Callable, Coroutine
from functools import wraps
from common.database.database import SessionLocal
import logging

# database decorator
def database_connect(func: Callable[..., Coroutine]) -> Callable[..., Coroutine]:
    @wraps(func)

    # inner wrapped vunction
    async def wrapper(*args, **kwargs):
        session = SessionLocal() # created session

        try:
            # safely runs inner function
            result = await func(*args, **kwargs, session=session)
            return result
        
        except Exception as e:
            # handles exceptions
            logging.error(f"An error occurred: {e}")

        finally:
            # closes sessions after running
            session.close()
    
    # returns the inner wrapped function
    return wrapper