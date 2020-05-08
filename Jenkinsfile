pipeline {
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
                 sh 'make test-func'
                 sh 'make test-perf'
             }
         }             
         stage('Publish') {
             steps {
                 sh 'docker build --tag=dog-classifier .'
                 sh 'docker image ls'
                 sh 'docker run -p 8000:80 dog-classifier'
                 sh 'docker tag dog-classifier udzhumok/dog-classifier:demo'
                 sh 'docker push udzhumok/dog-classifier:demo'
                 sh 'docker stop $(docker ps -a -q)'
                 sh 'docker rm $(docker ps -a -q)'
                 sh 'docker system prune -a'
             }
         }
         stage('Deploy') {
             steps {
                sh 'echo "Hello World"'                              
            }
         }                     
     }
}
