def call(String status, String pipelineName, String stageName) {
    def isSuccess = (status == 'SUCCESS')
    def emoji = isSuccess ? '✅' : '❌'
    def color = isSuccess ? 'green' : 'red'

    emailext(
        from: '70149156@student.uol.edu.pk',
        to: 'sikandar.hayat@is.uol.edu.pk',
        subject: "[${status}] ${emoji} ${pipelineName} Pipeline - Build #${env.BUILD_NUMBER}",
        body: """
            <h2 style='color:${color};'>${emoji} ${pipelineName} Pipeline — ${status}</h2>
            <table border='1' cellpadding='6'>
                <tr><td><b>Student</b></td><td>Syed Aun Ali Kazmi</td></tr>
                <tr><td><b>SAP ID</b></td><td>70149156</td></tr>
                <tr><td><b>Build</b></td><td>${env.BUILD_NUMBER}</td></tr>
                <tr><td><b>Branch</b></td><td>${env.BRANCH_NAME}</td></tr>
                <tr><td><b>Stage</b></td><td>${stageName}</td></tr>
                <tr><td><b>Status</b></td><td style='color:${color};'><b>${status}</b></td></tr>
                <tr><td><b>Console</b></td><td><a href='${env.BUILD_URL}'>${env.BUILD_URL}</a></td></tr>
            </table>
        """,
        mimeType: 'text/html'
    )
}
