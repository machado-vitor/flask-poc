pipeline {
    agent any
    options { skipDefaultCheckout(true) }

    stages {
        stage('Checkout') {
            steps {
              deleteDir()  // ensure a clean workspace
              checkout([
                $class: 'GitSCM',
                branches: [[name: '*/main']],               // adjust if your default branch isn’t main
                userRemoteConfigs: [[
                  url: 'https://github.com/machado-vitor/flask-poc.git',
                  credentialsId: 'ce5465c2-3536-4ecf-8f58-874611d5221d'
                ]],
                extensions: [[ $class: 'CleanBeforeCheckout' ]] // optional, keeps it clean
              ])
            }
        }
        stage('Install Dependencies') {
            steps {
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
                echo 'Building the project'
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

