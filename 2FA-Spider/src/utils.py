import functools
import time

from requests.exceptions import RequestException, HTTPError

from src.exceptions import MaxRetryRequestException, SearchException

def request_retry_with_backoff(max_retries=3, initial_retry_interval=1):
    def decorator(func):
        @functools.wraps(func)
        def _request_retry_with_backoff(*args, **kwargs):
            retries = 0
            retry_interval = initial_retry_interval

            while retries < max_retries:
                try:
                    result = func(*args, **kwargs)
                    return result
                except (RequestException, HTTPError, SearchException) as e:
                    retries += 1
                    if retries == max_retries:
                        raise MaxRetryRequestException(
                            f"Retry request failed after {max_retries} attempts."
                        )
                    print(f"RequestException: {str(e)}, retrying {retries}/{max_retries} in {retry_interval} seconds...")
                    time.sleep(retry_interval)

        return _request_retry_with_backoff

    return decorator