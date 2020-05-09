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
                sh 'pip3 install --user boto3 botocore'
                sh 'ansible-playbook -i inventory main.yml'
                sh 'pip3 install awscli --upgrade --user'
                sh 'curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp'
                sh 'sudo mv /tmp/eksctl /usr/local/bin'
                sh 'eksctl version'
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding',credentialsId: 'aws-creds',accessKeyVariable: 'AWS_ACCESS_KEY_ID',secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]){
                    sh 'aws eks --region us-east-2 update-kubeconfig --name kubernetes-cluster'
                }
                sh 'export KUBECONFIG=~/.kube/kubernetes-cluster'
                sh 'kubectl get svc'
            }
         }
         stage('Deploy application') {
             steps {  
                sh 'ansible-playbook -i inventory deploy.yml'
            }
         }                     
     }
}
