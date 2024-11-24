pipeline {
    agent any

    environment {
        CONTAINER_NAME = "friendly_raman"
        APP_PATH_IN_CONTAINER = "/app/html" // Adjust to your application path
        HOST_APP_PATH = "./app/html"       // Path to updated HTML files on the host
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Update Application Files') {
            steps {
                script {
                    echo "Copying updated HTML files into the container: ${CONTAINER_NAME}..."
                    sh '''
                        # Copy updated files into the container
                        docker cp ${HOST_APP_PATH}/ ${CONTAINER_NAME}:${APP_PATH_IN_CONTAINER}/
                    '''
                }
            }
        }

        stage('Restart Container') {
            steps {
                script {
                    echo "Restarting the container: ${CONTAINER_NAME}..."
                    sh '''
                        # Stop and restart the container
                        docker stop ${CONTAINER_NAME}
                        docker start ${CONTAINER_NAME}
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Application updated and container restarted successfully!'
        }
        failure {
            echo 'Update or restart failed. Check the logs for details.'
        }
    }
}
