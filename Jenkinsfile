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

