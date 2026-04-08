def call(String pipelineName, String failedStage) {
    emailext(
        to: '70149156@student.uol.edu.pk',
        subject: "[FAILURE] ${pipelineName} Pipeline - Build #${env.BUILD_NUMBER}",
        body: """
            <h2 style='color:red;'>${pipelineName} Pipeline FAILED</h2>
            <table>
                <tr><td><b>Student:</b></td><td>Syed Aun Ali Kazmi</td></tr>
                <tr><td><b>SAP ID:</b></td><td>70149156</td></tr>
                <tr><td><b>Build:</b></td><td>${env.BUILD_NUMBER}</td></tr>
                <tr><td><b>Branch:</b></td><td>${env.BRANCH_NAME}</td></tr>
                <tr><td><b>Failed Stage:</b></td><td>${failedStage}</td></tr>
                <tr><td><b>Console:</b></td><td><a href='${env.BUILD_URL}'>${env.BUILD_URL}</a></td></tr>
            </table>
        """,
        mimeType: 'text/html'
    )
}
