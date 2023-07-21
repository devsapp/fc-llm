function llmModeView(value) {

    const llmModelMap = {
        'chatglm2-6b-int4': 'chaglm2-6b int4量化版（推荐新手）',
        'chatglm2-6b': 'chaglm2-6b 原版（推荐企业）'
    }  

    return llmModelMap[value]
}

function llmAppView(value) {

    const llmAppMap = {
        'chatglm2-6b': 'chaglm2-6b 单独的问答系统',
        'langchain-ChatGLM': 'langchain-ChatGLM 支持添加自定义语料库的问答系统 '
    }  

    return llmAppMap[value]
}

module.exports = {
    llmModeView,
    llmAppView
};