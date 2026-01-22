import os
import time
import requests
import logging

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

def run_performance_test(endpoint, username, password, sentence, max_response_time=2.0):
    """Test API response time"""
    try:
        start_time = time.time()
        
        r = requests.get(
            url=f'http://{API_ADDRESS}:{API_PORT}{endpoint}',
            params={
                'username': username,
                'password': password,
                'sentence': sentence
            },
            timeout=10
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        test_status = 'SUCCESS' if response_time < max_response_time else 'FAILURE'
        
        output = f'''
============================
    Performance test
============================
request done at "{endpoint}"
| sentence="{sentence}"
| max allowed response time = {max_response_time}s
| actual response time = {response_time:.4f}s
==>  {test_status}
'''
        print(output)
        logging.info(output)
                
    except requests.exceptions.RequestException as e:
        error_msg = f"Error during performance test: {str(e)}\n"
        print(error_msg)
        logging.error(error_msg)

if __name__ == "__main__":
    # Wait for API to be ready
    time.sleep(5)
    
    logging.info("Starting performance tests")
    print("Starting performance tests")
    
    # Test response times for different endpoints
    run_performance_test('/v1/sentiment', 'alice', 'wonderland', 'I love this product')
    run_performance_test('/v1/sentiment', 'alice', 'wonderland', 'This is terrible')
    run_performance_test('/v2/sentiment', 'alice', 'wonderland', 'Great experience')
    run_performance_test('/permissions', 'alice', 'wonderland', '')
    
    logging.info("Performance tests completed")
    print("Performance tests completed")
