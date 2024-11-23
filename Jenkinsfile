pipeline {
    agent any

    environment {
        GIT_REPO = 'https://github.com/harsha-karatam/my-app.git' 
        DOCKER_IMAGE = 'harsha/my-python-app'
        DOCKER_CONTAINER_NAME = 'my-python-app-container'
        APP_PORT = '5000'
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning GitHub Repository...'
                git branch: 'main', url: "${GIT_REPO}"
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker Image...'
                sh 'docker build -t ${DOCKER_IMAGE}:latest .'
            }
        }

        stage('Deploy Application') {
            steps {
                script {
                    echo 'Stopping and Removing Existing Container (if any)...'
                    sh '''
                        docker stop ${DOCKER_CONTAINER_NAME} || true
                        docker rm ${DOCKER_CONTAINER_NAME} || true
                        sleep 5
                    '''
                    
                    echo 'Checking if Port is Available...'
                    // Check if port 5000 is in use
                    sh '''
                        if netstat -tuln | grep :${APP_PORT}; then
                            echo "Port ${APP_PORT} is in use. Exiting...";
                            exit 1;
                        fi
                    '''
                    
                    echo 'Running New Container...'
                    // Start a new container using the latest image
                    sh '''
                        docker run -d --name ${DOCKER_CONTAINER_NAME} -p ${APP_PORT}:${APP_PORT} ${DOCKER_IMAGE}:latest
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Application Deployed Successfully!'
        }
        failure {
            echo 'Build or Deployment Failed. Check the logs for details.'
        }
    }
}
