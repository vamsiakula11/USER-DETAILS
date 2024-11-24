pipeline {
    agent any

    environment {
        APP_NAME = "my-python-app"
        IMAGE_NAME = "harsha/my-python-app:latest"
        CONTAINER_NAME = "my-python-app-container"
        APP_PORT = "5000"
    }

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker Image...'
                sh 'docker build -t ${IMAGE_NAME} .'
            }
        }
        
        stage('Deploy Application') {
            steps {
                script {
                    echo 'Stopping and Removing Existing Container (if any)...'
                    sh '''
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                        sleep 5
                    '''
                    
                    echo 'Checking if Port is Available...'
                    sh '''
                        if netstat -tuln | grep -q :${APP_PORT}; then
                            echo "Port ${APP_PORT} is in use. Stopping process..."
                            lsof -i :${APP_PORT} | awk 'NR>1 {print $2}' | xargs kill -9 || true
                        fi
                    '''
                    
                    echo 'Starting New Docker Container...'
                    sh '''
                        docker run -d --name ${CONTAINER_NAME} -p ${APP_PORT}:${APP_PORT} ${IMAGE_NAME}
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment Successful!'
        }
        failure {
            echo 'Build or Deployment Failed. Check the logs for details.'
        }
    }
}

