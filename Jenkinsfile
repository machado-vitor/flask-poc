pipeline {
    agent any
    options { skipDefaultCheckout(true) }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'apt-get update && apt-get install -y python3-venv'
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh '. venv/bin/activate && pytest tests.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t flask-demo-app:latest .'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    # Detect OS
                    OS="$(uname -s | tr '[:upper:]' '[:lower:]')"

                    # Ensure minikube is running
                    minikube status || minikube start

                    # Make the local image available to minikube
                    if [ "${OS}" = "darwin" ]; then
                        # For macOS we need to handle image loading differently
                        # Build the image with a specific tag for minikube
                        eval $(minikube docker-env)
                        docker build -t flask-demo-app:latest .
                    else
                        # For Linux we can load the image directly
                        minikube image load flask-demo-app:latest
                    fi

                    # Deploy or upgrade the Helm chart from the app directory
                    cd app
                    helm upgrade --install flask-app ./helm/flask-app \
                      --set image.repository=flask-demo-app \
                      --set image.tag=latest \
                      --set image.pullPolicy=IfNotPresent

                    # Wait for deployment to complete
                    kubectl rollout status deployment/flask-app
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                echo "Application successfully deployed"
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}

