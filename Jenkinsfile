pipeline {
     environment {
        registry = "udzhumok/dog-classifier:demo"
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
         stage('Test') {
             steps {
                 sh 'make test'
             }
         }             
         stage('Publish') {
             steps {
                 script {
                    docker.build registry + ":$BUILD_NUMBER"
                 }
                 script {
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
