import time
import traceback

def with_retry(func, retries=3, delay=2):
    def wrapper(*args, **kwargs):
        for attempt in range(retries):
            try:
                return func(*args, **kwargs)

            except Exception as e:
                print(f"[{func.__name__}] attempt {attempt+1} failed")
                print(str(e))

                if attempt == retries - 1:
                    raise

                time.sleep(delay)

    return wrapper