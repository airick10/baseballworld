pipeline {
	agent {
	docker 
		{ 
		image 'python:3.12-slim' // comes with python & pip
		args '-v $HOME/.cache/pip:/root/.cache/pip' // optional pip cache 
		} 
	}
	stages {
	
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