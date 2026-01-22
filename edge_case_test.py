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

def run_edge_case_test(endpoint, username, password, sentence, expected_status, test_name):
    """Test edge cases"""
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
    Edge Case test: {test_name}
============================
request done at "{endpoint}"
| sentence="{sentence}"
| expected status = {expected_status}
| actual status = {status_code}
==>  {test_status}
'''
        print(output)
        logging.info(output)
                
    except requests.exceptions.RequestException as e:
        error_msg = f"Error during edge case test ({test_name}): {str(e)}\n"
        print(error_msg)
        logging.error(error_msg)

if __name__ == "__main__":
    # Wait for API to be ready
    time.sleep(5)
    
    logging.info("Starting edge case tests")
    print("Starting edge case tests")
    
    # Test empty sentence
    run_edge_case_test('/v1/sentiment', 'alice', 'wonderland', '', 200, 'Empty sentence')
    
    # Test very long sentence
    long_sentence = 'This is amazing! ' * 100
    run_edge_case_test('/v1/sentiment', 'alice', 'wonderland', long_sentence, 200, 'Very long sentence')
    
    # Test special characters
    run_edge_case_test('/v1/sentiment', 'alice', 'wonderland', '!@#$%^&*()', 200, 'Special characters')
    
    # Test numbers only
    run_edge_case_test('/v1/sentiment', 'alice', 'wonderland', '12345', 200, 'Numbers only')
    
    # Test mixed content
    run_edge_case_test('/v1/sentiment', 'alice', 'wonderland', 'Hello123!@#World', 200, 'Mixed content')
    
    logging.info("Edge case tests completed")
    print("Edge case tests completed")
