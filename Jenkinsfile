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
                    sh """ssh -o StrictHostKeyChecking=no $EC2_USER@$EC2_HOST << 'EOF'
if command -v sudo >/dev/null 2>&1; then
    sudo pkill -f "python manage.py runserver" || true
else
    pkill -f "python manage.py runserver" || true
fi

if [ -f "$APP_DIR/db.sqlite3" ]; then
    mkdir -p ~/backups
    cp "$APP_DIR/db.sqlite3" ~/backups/db.sqlite3.backup.\$(date +%Y%m%d%H%M%S)
    echo "Database backed up"
fi

rm -rf "$APP_DIR"
mkdir -p "$APP_DIR"
EOF"""
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
                    sh """ssh -o StrictHostKeyChecking=no $EC2_USER@$EC2_HOST << 'EOF'
set -e
cd "$APP_DIR"

python3 -m venv venv
. venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

python manage.py migrate
python manage.py collectstatic --noinput

nohup python manage.py runserver 0.0.0.0:$DJANGO_PORT > django.log 2>&1 &
echo \$! > django.pid
echo "Django server started on port $DJANGO_PORT with PID \$(cat django.pid)"
EOF"""
                }
            }
        }
    }
}
