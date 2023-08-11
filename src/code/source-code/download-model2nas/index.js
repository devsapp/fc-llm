'use strict';
const path = require('path');
const fs = require('fs-extra');
const downloads = require('@serverless-devs/downloads').default;


exports.handler = async (_event, _context, callback) => {
    const region = process.env.region || 'cn-hangzhou'
    const fileUrl = `https://serverless-ai-models-${region}.oss-${region}-internal.aliyuncs.com/chatglm2-6b-int4/pytorch_model.bin`;
    const filename = path.basename(fileUrl);
    const basePath = '/mnt/auto/llm/';
    const appDir = basePath + process.env.appPath;
    const modelDir = basePath + process.env.modelPath;
    if (!fs.existsSync(appDir)) {
        fs.ensureDirSync(appDir);
    }
    if (!fs.existsSync(modelDir)) {
        fs.ensureDirSync(modelDir);
    }
    const modelFile = path.join(modelDir, filename);

    if (process.env.modelPath !== 'chatglm2-6b-int4') {
        callback(null, 'do not need to download models');
        return;
    }
    if (fs.existsSync(modelFile)) {
        callback(null, 'fiExist');
    } else {
        try {
            await downloads(fileUrl, {
                dest: modelDir,
                filename,
                extract: true
            });
            callback(null, 'download success');
        } catch (e) {
            callback(null, e);
        }

    }
}
