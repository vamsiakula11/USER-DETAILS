pipeline {
    agent any

    environment {
        // Update these values with your configuration
        GIT_REPO = 'https://github.com/harsha-karatam/my-app.git' // Replace with your repo
        DOCKER_IMAGE = 'harsha/my-python-app'                    // Docker image name
        DOCKER_CONTAINER_NAME = 'my-python-app-container'        // Use a more descriptive container name
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
                sh '''
                    docker build -t ${DOCKER_IMAGE}:latest .
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                script {
                    echo 'Stopping and Removing Existing Container...'
                    sh '''
                        docker stop ${DOCKER_CONTAINER_NAME} || true
                        docker rm ${DOCKER_CONTAINER_NAME} || true
                    '''
                    
                    echo 'Running New Container...'
                    sh '''
                        docker run -d --name ${DOCKER_CONTAINER_NAME} -p 5000:5000 ${DOCKER_IMAGE}:latest
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
