pipeline {
    agent any

    environment {
        COMMIT_MESSAGE = """${sh(
            returnStdout: true,
            script: "git --no-pager log --format='medium' -1 ${GIT_COMMIT}"
        )}"""
        SETUP_PY_VERSION = """${sh(
            returnStdout: true,
            script: "python setup.py --version"
        )}"""

        DOCKER_REPO = "kadenlnelson/realvalidation"
        DOCKER_CREDENTIALS = "docker-hub-kadenlnelson"
    }

    stages {
        stage('Notify Slack') {
            steps {
                slackSend(color: '#FFFF00', message: "Build Started - ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)\n```${env.COMMIT_MESSAGE}```")
            }
        }

		    stage('docker build & push') {
            agent { docker { image 'docker:18.09.2' } }
            steps {
                script {
                    def image = docker.build("${DOCKER_REPO}")

                    docker.withRegistry('', "${DOCKER_CREDENTIALS}") {
                        image.push("${SETUP_PY_VERSION}")
                    }
                }

                slackSend (color: '#0db7ed', message: "Docker Image Built & Pushed - https://hub.docker.com/r/${DOCKER_REPO}\n```Try it out!\n$ docker run --rm ${DOCKER_REPO}```")
            }
        }
    }

    post {
        failure {
            slackSend (color: '#FF0000', message: "Build Failed! - ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)")
        }

        success {
            slackSend (color: '#00FF00', message: "Success! - ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)")
        }
    }
}
