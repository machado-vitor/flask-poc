pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'flask-demo-app'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                // Use explicit git checkout instead of 'checkout scm'
                git branch: 'main', url: 'https://github.com/machado-vitor/flask-poc.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                // Use Python within a virtual environment to avoid permission issues
                sh '''
                    python -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest tests.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    try {
                        sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                        sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
                    } catch (Exception e) {
                        echo "Docker build failed: ${e.message}"
                        currentBuild.result = 'FAILURE'
                        error "Docker build failed: ${e.message}"
                    }
                }
            }
        }

        stage('Deploy') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                script {
                    try {
                        sh "docker stop ${DOCKER_IMAGE} || true"
                        sh "docker rm ${DOCKER_IMAGE} || true"
                        sh "docker run -d -p 5001:5001 --name ${DOCKER_IMAGE} ${DOCKER_IMAGE}:latest"
                        echo "Application successfully deployed at port 5001"
                    } catch (Exception e) {
                        echo "Deployment failed: ${e.message}"
                        currentBuild.result = 'UNSTABLE'
                    }
                }
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
        unstable {
            echo 'Pipeline completed with issues!'
        }
        always {
            echo 'Cleaning up workspace...'
            sh 'rm -rf venv || true'
            cleanWs()
        }
    }
}
