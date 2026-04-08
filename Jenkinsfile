node {
    // 1. Pull the repository from GitHub into the Jenkins workspace
    checkout scm 

    def jenkinsfile_to_load = ""

    // 2. Check the branch or tag
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

    // 3. Load the correct file now that it actually exists in the workspace
    load jenkinsfile_to_load
}
