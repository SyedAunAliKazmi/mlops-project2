def jenkinsfile_to_load = ""

if (env.BRANCH_NAME == 'dev') {
    jenkinsfile_to_load = "Jenkinsfile.dev"
} else if (env.BRANCH_NAME == 'main') {
    jenkinsfile_to_load = "Jenkinsfile.preprod"
} else if (env.TAG_NAME?.startsWith('v')) {
    jenkinsfile_to_load = "Jenkinsfile.prod"
} else {
    currentBuild.result = 'ABORTED'
    error("No pipeline defined for branch: ${env.BRANCH_NAME}")
}

load jenkinsfile_to_load
