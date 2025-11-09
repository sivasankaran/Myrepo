pipeline {
  agent any

  options {
    ansiColor('xterm')
    timestamps()
  }

  stages {
    stage('Gather User Details') {
      steps {
        script {
          // Determine platform
          boolean onUnix = isUnix()

          // Find triggering user via build causes
          String triggeredBy = 'unknown'
          try {
            def causes = currentBuild?.rawBuild?.getCauses()
            if (causes) {
              for (c in causes) {
                if (c.class.simpleName == 'UserIdCause') {
                  triggeredBy = c.getUserId() ?: c.getUserName() ?: 'unknown'
                  break
                }
                if (c.class.simpleName == 'UpstreamCause') {
                  triggeredBy = c.shortDescription
                }
              }
            }
          } catch (ignored) {
            // ignore
          }

          // Jenkins Build User Vars plugin values if present
          String jenkinsUserId = env.BUILD_USER_ID ?: triggeredBy
          String jenkinsUser = env.BUILD_USER ?: ''
          String jenkinsUserEmail = env.BUILD_USER_EMAIL ?: ''

          // System/Agent-level information
          String whoamiOut
          String osInfo = ''
          String homeEnv = env.HOME ?: env.USERPROFILE ?: ''
          String userEnv = onUnix ? (env.USER ?: '') : (env.USERNAME ?: '')

          try {
            if (onUnix) {
              whoamiOut = sh(returnStdout: true, script: 'whoami 2>&1 || id -un').trim()
              osInfo = sh(returnStdout: true, script: 'uname -a || cat /etc/os-release || true').trim()
            } else {
              whoamiOut = bat(returnStdout: true, script: '@whoami').trim()
              osInfo = bat(returnStdout: true, script: '@ver').trim()
            }
          } catch (ignored2) {
            whoamiOut = 'unavailable'
          }

          echo '--- User and Environment Details ---'
          echo "Job: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
          echo "Build URL: ${env.BUILD_URL ?: ''}"
          echo "Jenkins node: ${env.NODE_NAME ?: 'master'}"
          echo "Triggered by (Jenkins userId): ${jenkinsUserId}"
          echo "Triggered by (Jenkins user display): ${jenkinsUser}"
          echo "Triggered by (email if available): ${jenkinsUserEmail}"
          echo "System user env: ${userEnv}"
          echo "whoami: ${whoamiOut}"
          echo "HOME: ${homeEnv}"
          echo "OS: ${osInfo}"
          echo "Workspace: ${env.WORKSPACE}"
          echo "Branch (if multibranch): ${env.BRANCH_NAME ?: ''}"
          echo "Git commit (if available): ${env.GIT_COMMIT ?: ''}"
          echo '------------------------------------'
        }
      }
    }
  }

  post {
    always {
      echo 'Build completed. User details logged above.'
    }
  }
}
