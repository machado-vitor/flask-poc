# Jenkins CI/CD Pipeline Demo

This project demonstrates a CI/CD pipeline using Jenkins to deploy a Flask application to Kubernetes using Helm.

## Application Overview

The application is a simple Flask API with the following endpoints:

- `/` - Renders an HTML page with information about the application
- `/api/hello` - Returns a JSON response with a "Hello, World!" message
- `/api/status` - Returns a JSON response with status information
- `/api/info` - Returns system information including hostname, IP address, platform, Python version, and environment

## Project Structure

- `app.py` - The main Flask application
- `templates/index.html` - The HTML template for the root route
- `tests.py` - Unit tests for the application
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker image definition
- `Jenkinsfile` - Jenkins pipeline definition
- `helm/flask-poc/` - Helm chart for deploying to Kubernetes

## CI/CD Pipeline

The CI/CD pipeline is defined in the `Jenkinsfile` and consists of the following stages:

1. **Checkout** - Checks out the code from the repository
2. **Install Dependencies** - Sets up a Python virtual environment and installs dependencies
3. **Run Tests** - Runs the unit tests to ensure the application works correctly
4. **Build and Push Docker Image** - Builds a Docker image and optionally pushes it to a registry
5. **Deploy to Kubernetes** - Deploys the application to Kubernetes using Helm

## Deployment

The application is deployed to Kubernetes using Helm. The Helm chart is located in the `helm/flask-poc/` directory and includes:

- Deployment - Manages the application pods
- Service - Provides network access to the application
- Ingress - Exposes the application to external traffic

## Running Locally

There are two ways to run the application locally:

### Option 1: Using the convenience script (macOS/Linux)

The easiest way to run the application is to use the provided convenience script:

```bash
# Make the script executable (if not already)
chmod +x run.sh

# Run the application
./run.sh
```

This script will automatically:
- Create a virtual environment if it doesn't exist
- Activate the virtual environment
- Install dependencies
- Run the application

To reinstall dependencies, use:
```bash
./run.sh --reinstall
```

### Option 2: Manual setup

If you prefer to run the commands manually or are using Windows:

1. Create and activate a virtual environment:
   ```bash
   # Create a virtual environment
   python3 -m venv venv
   
   # Activate the virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   # venv\Scripts\activate
   ```

2. Install dependencies in the virtual environment:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Access the application at http://localhost:5001

5. When you're done, deactivate the virtual environment:
   ```bash
   deactivate
   ```

## Running Tests

There are two ways to run the tests:

### Option 1: Using the convenience script (macOS/Linux)

The easiest way to run the tests is to use the provided convenience script:

```bash
# Make the script executable (if not already)
chmod +x run_tests.sh

# Run the tests
./run_tests.sh
```

This script will automatically:
- Create a virtual environment if it doesn't exist
- Activate the virtual environment
- Install dependencies
- Run the tests
- Deactivate the virtual environment when done

To reinstall dependencies, use:
```bash
./run_tests.sh --reinstall
```

### Option 2: Manual setup

If you prefer to run the commands manually or are using Windows:

1. Make sure your virtual environment is activated:
   ```bash
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   # venv\Scripts\activate
   ```

2. Run the tests:
   ```bash
   python -m pytest tests.py -v
   ```

## Deploying to Kubernetes

To deploy the application to Kubernetes:

1. Build the Docker image:
   ```
   docker build -t flask-demo-app:latest .
   ```

2. Install the Helm chart:
   ```
   helm upgrade --install flask-poc ./helm/flask-poc \
     --set image.repository=flask-demo-app \
     --set image.tag=latest \
     --set image.pullPolicy=IfNotPresent \
     --set ingress.hosts[0].host=flask-poc.example.com
   ```

## Infrastructure Management with OpenTofu

This project uses OpenTofu (formerly Terraform) for infrastructure management. The infrastructure code is located in the `terraform/` directory and includes:

1. **Separate Namespaces**:
   - `infrastructure` namespace for infrastructure components (Prometheus, Grafana)
   - `applications` namespace for application components (Flask app)

2. **Monitoring Stack**:
   - Prometheus for metrics collection
   - Grafana for metrics visualization
   - Default dashboards for application monitoring

3. **Automated Tests**:
   - Infrastructure tests using Terratest

### Setting Up Infrastructure

To set up the infrastructure:

1. Initialize OpenTofu:
   ```
   cd terraform
   tofu init
   ```

2. Apply the infrastructure configuration:
   ```
   tofu apply
   ```

3. To run infrastructure tests:
   ```
   cd terraform/test
   go test -v
   ```

## Monitoring

The application is integrated with Prometheus for monitoring. The following metrics are collected:

- HTTP request counts by method, endpoint, and status code
- HTTP request latency by method and endpoint

### Accessing Monitoring Tools

- Prometheus: Access via `http://prometheus-server.infrastructure.svc.cluster.local` within the cluster
- Grafana: Access via `http://grafana.infrastructure.svc.cluster.local` within the cluster
  - Default username: admin
  - Default password: admin (change this in production)

### Default Dashboards

A default dashboard for the Flask application is provided in Grafana, showing:
- Request rates by status code
- Request duration (95th percentile) by endpoint

## Recent Improvements

The following improvements have been made to the project:

1. **Fixed Helm Chart Templates**:
   - Removed duplicate Service definition in service.yaml
   - Removed duplicate Ingress definition in ingress.yaml
   - Ensured consistent use of helper templates

2. **Enhanced Jenkins Pipeline**:
   - Added environment variables for better configuration
   - Improved dependency installation with Python virtual environments
   - Enhanced Docker image building with proper tagging
   - Added support for pushing to a Docker registry
   - Improved Kubernetes deployment with proper configuration
   - Added cleanup steps to free resources

3. **Infrastructure and Monitoring**:
   - Added OpenTofu for infrastructure management
   - Implemented separate namespaces for infrastructure and applications
   - Added Prometheus and Grafana for monitoring
   - Implemented default monitoring integration for all applications
   - Added automated tests for infrastructure

These improvements make the project more maintainable, reliable, and production-ready.
