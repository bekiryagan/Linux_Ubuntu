# Sentiment Analysis API - Docker Project

A containerized sentiment analysis API with comprehensive testing suite built with FastAPI and Docker.

## Author
**Bekir Yagan** (bekiryagan)

## Project Description

This project demonstrates Docker containerization concepts including:
- Multi-container orchestration with Docker Compose
- Container networking and communication
- Health checks and service dependencies
- Logging and test automation

## Project Structure

\`\`\`
sentiment_api_test/
├── api.py                 # Main FastAPI application
├── auth_test.py           # Authentication tests
├── authz_test.py          # Authorization tests
├── content_test.py        # Content/Sentiment tests
├── performance_test.py    # Performance tests
├── edge_case_test.py      # Edge case tests
├── error_handling_test.py # Error handling tests
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile             # Docker image definition
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── logs/
    └── api_test.log       # Test execution logs
\`\`\`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check endpoint |
| `/permissions` | GET | Check user permissions |
| `/v1/sentiment` | GET | Sentiment analysis (v1) |
| `/v2/sentiment` | GET | Sentiment analysis (v2 - premium) |

## Users and Permissions

| Username | Password | v1 Access | v2 Access |
|----------|----------|-----------|-----------|
| alice | wonderland | Yes | Yes |
| bob | builder | Yes | No |

## Installation and Usage

### Prerequisites
- Docker
- Docker Compose

### Running the Project

1. Clone the repository:
\`\`\`bash
git clone https://github.com/bekiryagan/sentiment_api_test.git
cd sentiment_api_test
\`\`\`

2. Build and run the containers:
\`\`\`bash
docker-compose build
docker-compose up
\`\`\`

3. View the logs:
\`\`\`bash
cat logs/api_test.log
\`\`\`

4. Clean up:
\`\`\`bash
docker-compose down
\`\`\`

## Test Suites

### 1. Authentication Tests (auth_test.py)
Tests user authentication with valid and invalid credentials.

### 2. Authorization Tests (authz_test.py)
Tests user access permissions for different API versions.

### 3. Content Tests (content_test.py)
Tests sentiment analysis accuracy for positive and negative sentences.

### 4. Performance Tests (performance_test.py)
Tests API response times and performance under load.

### 5. Edge Case Tests (edge_case_test.py)
Tests handling of edge cases like empty inputs and special characters.

### 6. Error Handling Tests (error_handling_test.py)
Tests proper error responses and status codes.

## Docker Network

All services are connected via the `api_network` bridge network, enabling seamless communication between containers.

## License

This project is part of a Docker/Containerization course assignment.

## Acknowledgments

- FastAPI framework
- Docker and Docker Compose
- TextBlob for sentiment analysis
\`\`\`

Now let's create the 6 additional test files:

**Test 1: Performance Test**
