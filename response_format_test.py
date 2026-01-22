import os
import time
import requests
import logging
import json

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

def run_response_format_test(endpoint, username, password, sentence, expected_fields, test_name):
    """Test response format"""
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
        
        if r.status_code == 200:
            response_data = r.json()
            missing_fields = [field for field in expected_fields if field not in response_data]
            test_status = 'SUCCESS' if len(missing_fields) == 0 else 'FAILURE'
            fields_info = f"missing fields: {missing_fields}" if missing_fields else "all fields present"
        else:
            test_status = 'FAILURE'
            fields_info = f"unexpected status code: {r.status_code}"
        
        output = f'''
============================
    Response Format test: {test_name}
============================
request done at "{endpoint}"
| expected fields = {expected_fields}
| {fields_info}
==>  {test_status}
'''
        print(output)
        logging.info(output)
                
    except requests.exceptions.RequestException as e:
        error_msg = f"Error during response format test ({test_name}): {str(e)}\n"
        print(error_msg)
        logging.error(error_msg)

if __name__ == "__main__":
    # Wait for API to be ready
    time.sleep(5)
    
    logging.info("Starting response format tests")
    print("Starting response format tests")
    
    # Test sentiment response format
    run_response_format_test('/v1/sentiment', 'alice', 'wonderland', 'I love this', ['sentence', 'sentiment', 'polarity'], 'Sentiment v1 format')
    
    run_response_format_test('/v2/sentiment', 'alice', 'wonderland', 'I love this', ['sentence', 'sentiment', 'polarity'], 'Sentiment v2 format')
    
    # Test permissions response format
    run_response_format_test('/permissions', 'alice', 'wonderland', '', ['username', 'permissions'], 'Permissions format')
    
    # Test health response format
    run_response_format_test('/health', 'alice', 'wonderland', '', ['status'], 'Health format')
    
    logging.info("Response format tests completed")
    print("Response format tests completed")
