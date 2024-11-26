import requests
import concurrent.futures
import time
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def run_load_test(url, num_requests, concurrent_requests, results):
    start_time = time.time()
    request_details = []

    def send_request():
        try:
            response = requests.get(url)
            return {"url": response.url, "status_code": response.status_code, "response_time": response.elapsed.total_seconds(), "content": response.text[:200]}  # Truncate response content for brevity
        except requests.RequestException as e:
            return {"url": url, "status_code": "Error", "error": str(e)}

    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
        futures = [executor.submit(send_request) for _ in range(num_requests)]
        for future in concurrent.futures.as_completed(futures):
            request_details.append(future.result())

    end_time = time.time()
    duration = end_time - start_time

    # Store results
    results['duration'] = duration
    results['total_requests'] = num_requests
    results['concurrent_requests'] = concurrent_requests
    results['average_requests_per_second'] = num_requests / duration if duration > 0 else 0
    # results['requests'] = request_details  # Add request details
    logger.debug(results)
    logger.debug("test complted")
