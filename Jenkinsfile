pipeline {
    agent any

    environment {
        // Update these values with your configuration
        GIT_REPO = 'https://github.com/harsha-karatam/my-app.git' // GitHub repository URL
        DOCKER_IMAGE = 'harsha/my-python-app'                    // Docker image name
        DOCKER_CONTAINER_NAME = 'my-python-app-container'        // Docker container name
        APP_PORT = '5000'                                        // Application port inside the container
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning GitHub Repository...'
                // Use the environment variable for Git URL
                git branch: 'main', url: "${GIT_REPO}"
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker Image...'
                // Build Docker image using the provided Dockerfile
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
                    
                    echo 'Running New Container...'
                    sh '''
                        # Ensure no conflicting process is using the port
                        if lsof -i :${APP_PORT}; then
                            echo "Port ${APP_PORT} is in use. Exiting...";
                            exit 1;
                        fi
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
