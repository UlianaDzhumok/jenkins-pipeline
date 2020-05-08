pipeline {
     agent any
     stages {
         stage('Setup') {
             steps {
                 sh 'make setup'
                 sh 'make install'
             }
         }         
     }
}
