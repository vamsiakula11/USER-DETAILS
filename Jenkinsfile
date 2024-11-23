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
            // Ensure that port 5000 is not being used
            def portInUse = sh(script: "netstat -tuln | grep :${APP_PORT} || true", returnStatus: true)
            if (portInUse == 0) {
                echo "Port ${APP_PORT} is still in use. Exiting...";
                exit 1
            } else {
                echo "Port ${APP_PORT} is available."
            }

            echo 'Running New Container...'
            // Run the new container with the latest image
            sh '''
                docker run -d --name ${DOCKER_CONTAINER_NAME} -p ${APP_PORT}:${APP_PORT} ${DOCKER_IMAGE}:latest
            '''
        }
    }
}
