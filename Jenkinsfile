pipeline {
    agent any

    environment {
        APP_NAME = "babuuh/order-service"
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/Kihara-Njoroge/Simple-Order-Management-Service.git'
            }
        }

        stage('Build and Tag') {
            steps {
                script {
                    echo "Building Docker Image."

                    // Docker login and build
                    withCredentials([usernamePassword(credentialsId: 'DockerHubCredentials', passwordVariable: 'DOCKERHUB_PASSWORD', usernameVariable: 'DOCKERHUB_USERNAME')]) {
                        sh "echo \$DOCKERHUB_PASSWORD | docker login -u \$DOCKERHUB_USERNAME --password-stdin"
                        sh "docker build -t ${APP_NAME}:latest ."
                    }
                }
            }
        }

        stage('Scan Docker Image') {
            steps {
                script {
                    // Run Trivy to scan the Docker image
                    def trivyOutput = sh(script: "trivy image ${APP_NAME}:latest", returnStdout: true).trim()

                    // Display Trivy scan results
                    echo "${trivyOutput}"

                    // Check if vulnerabilities were found
                    if (trivyOutput.contains("Total: 0")) {
                        echo "No vulnerabilities found in the Docker image."
                    } else {
                        error "Vulnerabilities found in the Docker image."
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    // Push Docker image to Docker Hub
                    withCredentials([usernamePassword(credentialsId: 'DockerHubCredentials', passwordVariable: 'DOCKERHUB_PASSWORD', usernameVariable: 'DOCKERHUB_USERNAME')]) {
                        sh "docker push ${APP_NAME}:latest"
                    }
                }
            }
        }
    }
}
