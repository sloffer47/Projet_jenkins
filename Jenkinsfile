pipeline {
    agent any
    
    environment {
        EC2_HOST = '13.61.100.227'
        EC2_USER = 'ec2-user'
        APP_NAME = 'gestion-etudiants'
        GITHUB_REPO = 'https://github.com/sloffer47/Projet_jenkins.git'
        SSH_CREDENTIALS = 'ec2-ssh-key'
        DOCKER_IMAGE = 'gestion-etudiants:latest'
        APP_PORT = '8064'
    }
    
    stages {
        stage('🔍 Pull Code from GitHub') {
            steps {
                echo 'Récupération du code depuis GitHub...'
                git branch: 'main', url: "${GITHUB_REPO}"
            }
        }
        
        stage('📋 Verify Files') {
            steps {
                echo 'Vérification des fichiers du projet...'
                sh 'ls -la'
                sh 'cat Dockerfile || echo "Dockerfile non trouvé"'
            }
        }
        
        stage('🚀 Deploy to EC2 Server') {
            steps {
                echo 'Déploiement sur le serveur EC2 AWS...'
                sshagent(credentials: ["${SSH_CREDENTIALS}"]) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} '
                            echo "🧹 Nettoyage des anciens containers..."
                            docker stop ${APP_NAME} 2>/dev/null || true
                            docker rm ${APP_NAME} 2>/dev/null || true
                            docker rmi ${DOCKER_IMAGE} 2>/dev/null || true
                            
                            echo "📥 Mise à jour du code..."
                            if [ -d "${APP_NAME}" ]; then
                                cd ${APP_NAME}
                                git pull origin main
                                cd ..
                            else
                                git clone ${GITHUB_REPO}
                            fi
                            
                            echo "🔨 Construction de l image Docker..."
                            cd ${APP_NAME}
                            docker build -t ${DOCKER_IMAGE} .
                            
                            echo "🚀 Lancement du nouveau container..."
                            docker run -d \\
                                --name ${APP_NAME} \\
                                -p ${APP_PORT}:5000 \\
                                --restart unless-stopped \\
                                ${DOCKER_IMAGE}
                            
                            echo "⏳ Attente du démarrage..."
                            sleep 10
                            
                            echo "✅ Vérification du déploiement..."
                            if docker ps | grep -q ${APP_NAME}; then
                                echo "SUCCESS: Application déployée avec succès!"
                                docker ps | grep ${APP_NAME}
                            else
                                echo "ERROR: Problème lors du déploiement"
                                docker logs ${APP_NAME}
                                exit 1
                            fi
                            
                            echo "🧹 Nettoyage des images inutiles..."
                            docker image prune -f
                        '
                    """
                }
            }
        }
        
        stage('🏥 Health Check') {
            steps {
                echo 'Test de santé de l application...'
                script {
                    sleep(5)
                    try {
                        def response = sh(
                            script: "curl -s -o /dev/null -w '%{http_code}' http://${EC2_HOST}:${APP_PORT}",
                            returnStdout: true
                        ).trim()
                        
                        if (response == '200') {
                            echo "✅ SUCCESS: Application accessible!"
                        } else {
                            echo "⚠️ WARNING: Code de réponse HTTP: ${response}"
                        }
                    } catch (Exception e) {
                        echo "⚠️ WARNING: Impossible de tester la connectivité (normal si pas de route de santé)"
                    }
                }
            }
        }
    }
    
    post {
        success {
            echo '''
            🎉🎉🎉 DÉPLOIEMENT RÉUSSI! 🎉🎉🎉
            
            📱 Votre application est maintenant accessible à :
            🌐 http://13.61.100.227:8064
            
            📊 Pour vérifier l état :
            docker ps
            docker logs gestion-etudiants
            '''
        }
        
        failure {
            echo '''
            ❌❌❌ ÉCHEC DU DÉPLOIEMENT ❌❌❌
            
            🔍 Vérifiez les logs ci-dessus pour identifier le problème.
            
            🛠️ Commandes de dépannage sur le serveur :
            ssh -i serveur_KEY.pem ec2-user@13.61.100.227
            docker logs gestion-etudiants
            docker ps -a
            '''
        }
        
        always {
            echo '🏁 Pipeline terminé.'
        }
    }
}