pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKER_IMAGE = 'guilherme123012/comp314'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Login to DockerHub') {
            steps {
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
            }
        }

        stage('Push Image to DockerHub') {
            steps {
                sh 'docker push $DOCKER_IMAGE'
            }
        }

        stage('Deploy Container') {
            steps {
                echo 'Deploying container'
                sh '''
                    docker stop simple-webpage-container || true
                    docker rm simple-webpage-container || true
                    docker run -d --restart always -p 80:80 --name simple-webpage-container $DOCKER_IMAGE
                '''
            }
        }
    }

    post {
        always {
            sh 'docker logout'
        }
    }
}