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

def run_input_validation_test(endpoint, username, password, sentence, expected_status, test_name):
    """Test input validation"""
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
        
        status_code = r.status_code
        test_status = 'SUCCESS' if status_code == expected_status else 'FAILURE'
        
        output = f'''
============================
    Input Validation test: {test_name}
============================
request done at "{endpoint}"
| username="{username}"
| password="{password}"
| sentence="{sentence[:50]}..."
| expected status = {expected_status}
| actual status = {status_code}
==>  {test_status}
'''
        print(output)
        logging.info(output)
                
    except requests.exceptions.RequestException as e:
        error_msg = f"Error during input validation test ({test_name}): {str(e)}\n"
        print(error_msg)
        logging.error(error_msg)

if __name__ == "__main__":
    # Wait for API to be ready
    time.sleep(5)
    
    logging.info("Starting input validation tests")
    print("Starting input validation tests")
    
    # Test valid input
    run_input_validation_test('/v1/sentiment', 'alice', 'wonderland', 'This is great', 200, 'Valid input')
    
    # Test username with spaces
    run_input_validation_test('/v1/sentiment', 'alice ', 'wonderland', 'Test', 403, 'Username with spaces')
    
    # Test password with spaces
    run_input_validation_test('/v1/sentiment', 'alice', ' wonderland', 'Test', 403, 'Password with spaces')
    
    # Test unicode characters in sentence
    run_input_validation_test('/v1/sentiment', 'alice', 'wonderland', 'This is great', 200, 'Unicode sentence')
    
    # Test sentence with newlines
    run_input_validation_test('/v1/sentiment', 'alice', 'wonderland', 'Line1\nLine2', 200, 'Sentence with newlines')
    
    logging.info("Input validation tests completed")
    print("Input validation tests completed")
