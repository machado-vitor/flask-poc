pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'flask-demo-app'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Install Dependencies') {
            steps {
                script {
                    try {
                        // Use Python within a virtual environment to avoid permission issues
                        sh '''
                            python -m venv venv || python3 -m venv venv
                            . venv/bin/activate
                            pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                    } catch (Exception e) {
                        echo "Failed to install dependencies: ${e.message}"
                        error "Failed to install dependencies: ${e.message}"
                    }
                }
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

        stage('Build Simulation') {
            steps {
                script {
                    try {
                        echo "Simulating build process for ${DOCKER_IMAGE}:${DOCKER_TAG}"
                        echo "Checking application artifacts..."
                        sh "ls -la"
                        echo "Build simulation successful"
                    } catch (Exception e) {
                        echo "Build simulation failed: ${e.message}"
                        currentBuild.result = 'FAILURE'
                        error "Build simulation failed: ${e.message}"
                    }
                }
            }
        }

        stage('Deploy Simulation') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                script {
                    try {
                        echo "Simulating deployment of ${DOCKER_IMAGE} application"
                        echo "Copying application files to simulated production environment..."
                        sh "mkdir -p deploy-simulation"
                        sh "cp -r *.py deploy-simulation/"
                        sh "cp -r requirements.txt deploy-simulation/"

                        echo "Starting simulated application service..."
                        echo "Verifying deployment..."
                        sh "ls -la deploy-simulation"

                        echo "Application successfully deployed in simulation environment"
                    } catch (Exception e) {
                        echo "Simulated deployment failed: ${e.message}"
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
        }
    }
}

