pipeline {
    agent any

    tools {
        python 'Python-3.12'
    }

    stages {
        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt pytest-cov pytest-asyncio'
            }
        }

        stage('Unit Tests') {
            steps {
                sh 'python -m pytest test/unit/ -v --tb=short --cov=bot --cov=api --cov=page --cov-report=term-missing --junitxml=reports/unit-results.xml --alluredir=allure-results'
            }
            post {
                always {
                    junit 'reports/unit-results.xml'
                }
            }
        }

        stage('Integration Tests') {
            steps {
                sh 'python -m pytest test/ --headless -v --ignore=test/unit --junitxml=reports/integration-results.xml --alluredir=allure-results'
            }
            post {
                always {
                    junit 'reports/integration-results.xml'
                }
            }
        }

        stage('Allure Report') {
            steps {
                allure includeProperties: false,
                       jdk: '',
                       results: [[path: 'allure-results']]
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
