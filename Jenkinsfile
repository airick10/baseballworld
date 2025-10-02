pipeline {
	agent any
	stages {
		stage('Prep Python (ephemeral)') {
		  steps {
			sh '''
			  sudo apt-get update -y
			  sudo apt-get install -y python3 python3-venv python3-pip
			'''
		  }
		}
	
		stage('Checkout') {
			steps {
				git url: 'https://github.com/airick10/baseballworld', branch: 'main'
				sh "ls -ltr"
			}
		}
		
		stage('Setup') {
			steps {
				sh "pip install -r requirements.txt"
			}
		}
	}
}