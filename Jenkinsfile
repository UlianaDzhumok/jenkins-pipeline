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
             
     }
}
