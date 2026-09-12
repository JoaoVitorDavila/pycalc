pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKERHUB_USER = 'jvdavila'
        IMAGE_NAME = "${DOCKERHUB_USER}/pycalc"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                sh 'pip3 install --break-system-packages -r requirements.txt'
            }
        }

        stage('Run tests') {
            steps {
                sh 'cd app && python3 -m pytest tests/ -v'
            }
        }

        stage('Build Docker image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                sh "docker push ${IMAGE_NAME}:latest"
            }
        }

        stage('Deploy to AWS with Ansible') {
            steps {
                sh '''
                    cp /var/jenkins_home/pycalc-key.pem /tmp/pycalc-key.pem
                    chmod 600 /tmp/pycalc-key.pem
                    ansible-playbook -i ansible/inventory.ini ansible/deploy.yml -e image_tag=$IMAGE_TAG
                '''
            }
        }
    }

    post {
        success {
            echo "Deploy finished! Visit http://56.124.16.161:30080"
        }
        failure {
            echo "Pipeline failed — check the stage logs above."
        }
    }
}
