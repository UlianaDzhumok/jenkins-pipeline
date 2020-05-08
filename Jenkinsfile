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
         stage('Create Cluster') {
             steps {
                sh 'curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -'
                sh 'sudo touch /etc/apt/sources.list.d/kubernetes.list' 
                sh 'echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list'
                sh 'sudo apt-get update'
                sh 'sudo apt-get install -y kubectl'
                sh 'sudo apt-get install ansible'
                sh 'pip3 install boto'
                sh 'pip3 install botocore'
                sh 'ansible-playbook -i inventory main.yml'
            }
         }
         stage('Deploy application') {
             steps {
                sh 'echo "Hello World" '
            }
         }                     
     }
}
