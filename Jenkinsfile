pipeline {
	agent any
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