'use strict';
const path = require('path');
const fs = require('fs');
const downloads = require('@serverless-devs/downloads').default;


exports.handler = async (_event, _context, callback) => {
    const region = process.env.region || 'cn-hangzhou'
    const fileUrl = `https://serverless-ai-models-${region}.oss-${region}-internal.aliyuncs.com/chatglm2-6b-int4/pytorch_model.bin`;
    const filename = path.basename(fileUrl);
    const downloadDir = '/mnt/auto/llm/' + process.env.modelPath;
    const modelFile = path.join(downloadDir, filename);
    if (fs.existsSync(modelFile)) {
        callback(null, 'fiExist');
    } else {
        await downloads(fileUrl, {
            dest: downloadDir,
            filename,
            extract: true
        });
        callback(null, 'download success');
    }
}
