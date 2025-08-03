pipeline {
    agent any

    environment {
        // Define environment variables
        APP_NAME = 'flask-demo-app'
        DOCKER_REGISTRY = 'docker.io/yourusername' // Replace with your registry
        IMAGE_TAG = "${env.BUILD_NUMBER}-${env.GIT_COMMIT.substring(0,7)}"
        // Default to not deploying to Kubernetes
        KUBERNETES_DEPLOY = 'false'
    }

    options {
        skipDefaultCheckout(true)
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                // Use a more portable approach for Python dependencies
                sh '''
                    # Create and activate virtual environment
                    python3 -m venv .venv
                    . .venv/bin/activate

                    # Install dependencies
                    pip install --upgrade pip
                    pip install -r app/requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    # Activate virtual environment and run tests
                    . .venv/bin/activate
                    cd app
                    python -m pytest tests.py -v
                '''
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    // Build the Docker image with proper tagging
                    sh """
                        cd app
                        docker build -t ${APP_NAME}:${IMAGE_TAG} -t ${APP_NAME}:latest .
                    """

                    // Optional: Push to a registry if configured
                    // Uncomment the following lines when ready to push to a registry
                    /*
                    withCredentials([usernamePassword(credentialsId: 'docker-registry-credentials',
                                                     usernameVariable: 'DOCKER_USER',
                                                     passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh """
                            echo \${DOCKER_PASSWORD} | docker login -u \${DOCKER_USER} --password-stdin
                            docker tag ${APP_NAME}:${IMAGE_TAG} ${DOCKER_REGISTRY}/${APP_NAME}:${IMAGE_TAG}
                            docker tag ${APP_NAME}:${IMAGE_TAG} ${DOCKER_REGISTRY}/${APP_NAME}:latest
                            docker push ${DOCKER_REGISTRY}/${APP_NAME}:${IMAGE_TAG}
                            docker push ${DOCKER_REGISTRY}/${APP_NAME}:latest
                        """
                    }
                    */
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    try {
                        // Try to load kubeconfig credentials
                        withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                            env.KUBERNETES_DEPLOY = 'true'

                            // Set up kubeconfig
                            sh "mkdir -p ~/.kube"
                            sh "cp ${KUBECONFIG} ~/.kube/config"

                            // Deploy using Helm to the applications namespace
                            sh """
                                cd app
                                helm upgrade --install ${APP_NAME} ./helm/flask-poc \
                                  --namespace applications \
                                  --create-namespace \
                                  --set image.repository=${APP_NAME} \
                                  --set image.tag=${IMAGE_TAG} \
                                  --set image.pullPolicy=IfNotPresent \
                                  --set ingress.hosts[0].host=${APP_NAME}.example.com \
                                  --set prometheus.enabled=true
                            """

                            // Verify deployment
                            sh "kubectl rollout status deployment/${APP_NAME}"

                            // Display service information
                            sh "kubectl get svc,ing -l app.kubernetes.io/name=${APP_NAME}"
                        }
                    } catch (Exception e) {
                        // If kubeconfig credential doesn't exist or any other error occurs
                        echo "Skipping Kubernetes deployment: ${e.message}"
                        echo "To deploy to Kubernetes, make sure the 'kubeconfig' credential is configured in Jenkins."
                        // Don't fail the build
                        env.KUBERNETES_DEPLOY = 'false'
                    }
                }
            }
        }
    }

    post {
        success {
            script {
                if (env.KUBERNETES_DEPLOY == 'true') {
                    echo "Pipeline completed successfully! Application deployed to Kubernetes."
                } else {
                    echo "Pipeline completed successfully! Application built and tested, but not deployed to Kubernetes."
                    echo "To deploy to Kubernetes, make sure the 'kubeconfig' credential is configured in Jenkins."
                }
            }
        }
        failure {
            echo "Pipeline failed! Check the logs for details."
        }
        always {
            // Clean up
            node('') {  // Empty string label means use any available node
                sh "rm -rf .venv"
                sh "docker system prune -f"
            }
        }
    }
}
