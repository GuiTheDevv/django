pipeline {
    agent any

    environment {
        EC2_USER = 'ubuntu'
        EC2_HOST = '18.217.181.167'
        APP_DIR = '/home/ubuntu/my-django-app'
        SSH_KEY_ID = 'ec2-ssh-key'
        DJANGO_PORT = '8000'
    }

    stages {
        stage('Clean EC2 Directory') {
            steps {
                sshagent([env.SSH_KEY_ID]) {
                    sh """
                    ssh -o StrictHostKeyChecking=no $EC2_USER@$EC2_HOST '
                        # Stop any running Django server
                        pkill -f "python manage.py runserver" || true
                        
                        # Remove the existing directory and recreate it
                        rm -rf $APP_DIR
                        mkdir -p $APP_DIR
                    '
                    """
                }
            }
        }

        stage('Upload Project to EC2') {
            steps {
                sshagent([env.SSH_KEY_ID]) {
                    sh """
                    scp -o StrictHostKeyChecking=no -r * $EC2_USER@$EC2_HOST:$APP_DIR/
                    """
                }
            }
        }

        stage('Deploy Django App') {
            steps {
                sshagent([env.SSH_KEY_ID]) {
                    sh """
                    ssh -o StrictHostKeyChecking=no $EC2_USER@$EC2_HOST "
                        set -e
                        cd $APP_DIR
                        # Setup virtual environment
                        python3 -m venv venv
                        source venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                        
                        # Run Django management commands
                        python manage.py migrate
                        python manage.py collectstatic --noinput
                        
                        # Start Django server
                        nohup python manage.py runserver 0.0.0.0:$DJANGO_PORT > django.log 2>&1 &
                        echo 'Django server started on port $DJANGO_PORT'
                    "
                    """
                }
            }
        }
    }
}