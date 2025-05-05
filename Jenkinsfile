pipeline {
    agent any

    environment {
        EC2_USER = 'ubuntu'
        EC2_HOST = '18.217.181.167'
        REMOTE_HOME = '/home/ubuntu'
        PROJECT_NAME = 'my-django-app'
        APP_DIR = "${REMOTE_HOME}/${PROJECT_NAME}"
        SSH_KEY_ID = 'ec2-ssh-key'
        DJANGO_PORT = '8000'
    }

    stages {
        stage('Prepare EC2 Directory') {
            steps {
                sshagent([env.SSH_KEY_ID]) {
                    sh """
                    ssh -o StrictHostKeyChecking=no $EC2_USER@$EC2_HOST 'mkdir -p $APP_DIR'
                    """
                }
            }
        }

        stage('Upload Project to EC2') {
            steps {
                sshagent([env.SSH_KEY_ID]) {
                    sh """
                    scp -o StrictHostKeyChecking=no -r ${PROJECT_NAME} $EC2_USER@$EC2_HOST:$REMOTE_HOME
                    """
                }
            }
        }

        stage('Deploy Django App') {
            steps {
                sshagent([env.SSH_KEY_ID]) {
                    sh """
                    ssh -o StrictHostKeyChecking=no $EC2_USER@$EC2_HOST '
                        set -e
                        sudo apt update
                        sudo apt install -y python3.12-venv
                        cd $APP_DIR
                        python3 -m venv venv
                        source venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                        python manage.py migrate
                        python manage.py collectstatic --noinput
                        nohup python manage.py runserver 0.0.0.0:$DJANGO_PORT &
                    '
                    """
                }
            }
        }
    }
}
