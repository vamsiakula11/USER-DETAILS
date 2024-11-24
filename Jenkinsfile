pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Update Running Container') {
            steps {
                script {
                    echo 'Copying updated files into the running container...'
                    sh 'docker cp ./app/ my-python-app-container:/app/'

                    echo 'Restarting application inside the container...'
                    sh 'docker exec my-python-app-container systemctl restart my-service || pkill -f "python app.py" && python app.py &'
                }
            }
        }
    }

    post {
        success {
            echo 'Application updated successfully without restarting the container!'
        }
        failure {
            echo 'Update failed. Check logs for details.'
        }
    }
}
