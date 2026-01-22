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

def run_error_handling_test(endpoint, params, expected_status, test_name):
    """Test error handling"""
    try:
        r = requests.get(
            url=f'http://{API_ADDRESS}:{API_PORT}{endpoint}',
            params=params,
            timeout=10
        )
        
        status_code = r.status_code
        test_status = 'SUCCESS' if status_code == expected_status else 'FAILURE'
        
        output = f'''
============================
    Error Handling test: {test_name}
============================
request done at "{endpoint}"
| params={params}
| expected status = {expected_status}
| actual status = {status_code}
==>  {test_status}
'''
        print(output)
        logging.info(output)
                
    except requests.exceptions.RequestException as e:
        error_msg = f"Error during error handling test ({test_name}): {str(e)}\n"
        print(error_msg)
        logging.error(error_msg)

if __name__ == "__main__":
    # Wait for API to be ready
    time.sleep(5)
    
    logging.info("Starting error handling tests")
    print("Starting error handling tests")
    
    # Test missing username
    run_error_handling_test('/permissions', {'password': 'wonderland'}, 422, 'Missing username')
    
    # Test missing password
    run_error_handling_test('/permissions', {'username': 'alice'}, 422, 'Missing password')
    
    # Test invalid credentials
    run_error_handling_test('/permissions', {'username': 'invalid', 'password': 'invalid'}, 403, 'Invalid credentials')
    
    # Test missing sentence parameter
    run_error_handling_test('/v1/sentiment', {'username': 'alice', 'password': 'wonderland'}, 422, 'Missing sentence')
    
    # Test unauthorized access to v2
    run_error_handling_test('/v2/sentiment', {'username': 'bob', 'password': 'builder', 'sentence': 'test'}, 403, 'Unauthorized v2 access')
    
    logging.info("Error handling tests completed")
    print("Error handling tests completed")
