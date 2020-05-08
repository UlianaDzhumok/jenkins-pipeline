pipeline {
     environment {
        registry = "udzhumok/dog-classifier"
        registryCredential = 'DockerHub'
        dockerImage = ''
     }
     agent any
     stages {
         stage('Setup Environment') {
             steps {
                 sh 'make setup'
                 sh 'make install'
             }
         }
         stage('Code Analysis') {
             steps {
                 sh 'make lint'
                 aquaMicroscanner imageName: 'alpine:latest', notCompliesCmd: 'exit 1', onDisallowed: 'fail', outputFormat: 'json'
             }
         }
         stage('Test Application') {
             steps {
                 sh 'make test'
             }
         }             
         stage('Publish Docker image') {
             steps {
                 script {
                    dockerImage=docker.build registry + ":$BUILD_NUMBER"
                    docker.withRegistry( '', registryCredential ) {
                        dockerImage.push()
                    }
                 }
                 sh "docker rmi $registry:$BUILD_NUMBER"
             }
         }
         stage('Deploy') {
             steps {
                sh 'echo "Hello World"'                              
            }
         }                     
     }
}
