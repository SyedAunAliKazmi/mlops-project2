def ingestData() {
    sh 'python3 src/data_ingest.py'
}

def trainModel() {
    sh 'python3 src/train.py'
}

def deployModel(String modelUri) {
    sh "python3 src/deploy_model.py '${modelUri}'"
}

def testModel(String modelUri) {
    sh "python3 src/test_model.py '${modelUri}'"
}

def registerModel(String alias) {
    def runId = readFile('run_id.txt').trim()
    sh "python3 src/register_model.py '${runId}' '${alias}'"
}

def loadModel(String alias) {
    sh "python3 src/load_model.py '${alias}'"
}

def updateAlias(String oldAlias, String newAlias) {
    def version = readFile('model_version.txt').trim()
    sh "python3 src/update_alias.py '${version}' '${oldAlias}' '${newAlias}'"
}

def getRunId() {
    return readFile('run_id.txt').trim()
}
