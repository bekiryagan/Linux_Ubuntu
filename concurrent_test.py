import os
import time
import requests
import logging
import concurrent.futures

# Set up logging
os.makedirs('/app/logs', exist_ok=True)
logging.basicConfig(
    filename='/app/logs/api_test.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Set up constants
API_ADDRESS = 'api'
API_PORT = 8000

def make_request(request_id, endpoint, username, password, sentence):
    """Make a single request"""
    try:
        r = requests.get(
            url=f'http://{API_ADDRESS}:{API_PORT}{endpoint}',
            params={
                'username': username,
                'password': password,
                'sentence': sentence
            },
            timeout=10
        )
        return (request_id, r.status_code, True)
    except Exception as e:
        return (request_id, 0, False)

def run_concurrent_test(num_requests, endpoint, username, password, sentence):
    """Test concurrent requests"""
    try:
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
            futures = [
                executor.submit(make_request, i, endpoint, username, password, sentence)
                for i in range(num_requests)
            ]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        end_time = time.time()
        total_time = end_time - start_time
        
        successful = sum(1 for r in results if r[2] and r[1] == 200)
        failed = num_requests - successful
        
        test_status = 'SUCCESS' if successful == num_requests else 'FAILURE'
        
        output = f'''
============================
    Concurrent test
============================
request done at "{endpoint}"
| total requests = {num_requests}
| successful = {successful}
| failed = {failed}
| total time = {total_time:.4f}s
==>  {test_status}
'''
        print(output)
        logging.info(output)
                
    except Exception as e:
        error_msg = f"Error during concurrent test: {str(e)}\n"
        print(error_msg)
        logging.error(error_msg)

if __name__ == "__main__":
    # Wait for API to be ready
    time.sleep(5)
    
    logging.info("Starting concurrent tests")
    print("Starting concurrent tests")
    
    # Test with 5 concurrent requests
    run_concurrent_test(5, '/v1/sentiment', 'alice', 'wonderland', 'I love this')
    
    # Test with 10 concurrent requests
    run_concurrent_test(10, '/v1/sentiment', 'alice', 'wonderland', 'Great product')
    
    logging.info("Concurrent tests completed")
    print("Concurrent tests completed")
