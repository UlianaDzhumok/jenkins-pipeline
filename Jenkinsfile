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
         stage('Deploy Cluster') {
             steps {
                sh 'curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -'
                sh 'sudo touch /etc/apt/sources.list.d/kubernetes.list' 
                sh 'echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list'
                sh 'sudo apt-get update'
                sh 'sudo apt-get install -y kubectl'
                sh 'sudo apt-get install ansible'
                sh 'pip3 install boto'
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding',credentialsId: 'aws-creds',accessKeyVariable: 'AWS_ACCESS_KEY_ID',secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]){
                    sh '''
                        mkdir -p ~/.aws
                        echo "[default]" >~/.aws/credentials
                        echo "aws_access_key_id=${AWS_ACCESS_KEY_ID}">>~/.aws/credentials
                        echo "aws_secret_access_key=${AWS_SECRET_ACCESS_KEY}">>~/.aws/credentials
                        echo "[default]" >~/.boto
                        echo "aws_access_key_id=${AWS_ACCESS_KEY_ID}">>~/.boto
                        echo "aws_secret_access_key=${AWS_SECRET_ACCESS_KEY}">>~/.boto
                    '''
                }
                sh 'git clone https://github.com/kubernetes-incubator/kubespray'
                sh 'ansible-playbook -i inventory.cfg -b -v cluster.yml'
                sh 'kubectl create -f deployment.yml'
                sh 'kubectl get pods'
            }
         }                     
     }
}
