import time


# """Safely call a function with retry logic."""
def safe_api_call(func, retries=3, delay=2, **kwargs):
    """
    Safely call a function with retry logic.

    Args:
        func (_type_): Function to execute
        retries (int, optional): Number of retries. Defaults to 3.
        delay (int, optional): Delay in seconds. Defaults to 2.

    Returns:
        function call result: The original function call result.
    """

    for attempt in range(retries):
        try:
            return func(**kwargs)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise
