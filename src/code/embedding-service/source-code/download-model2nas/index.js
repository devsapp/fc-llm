'use strict';
const path = require('path');
const fs = require('fs');
const downloads = require('@serverless-devs/downloads').default;

exports.handler = async (_event, _context, callback) => {
  const region = process.env.region || 'cn-hangzhou';
  const embedding_model_name = process.env.EMBEDDING_MODEL_NAME || 'bge-large-zh' // text2vec-large-chinese
  const fileUrl = `https://serverless-ai-models-${region}.oss-${region}-internal.aliyuncs.com/${embedding_model_name}/pytorch_model.bin`;
  const filename = path.basename(fileUrl);
  const downloadDir = `/mnt/auto/embedding/${embedding_model_name}`;
  if (!fs.existsSync(downloadDir)) {
    fs.mkdirSync(downloadDir, { recursive: true });
  }
  const sdCkpt = path.join(downloadDir, filename);
  if (fs.existsSync(sdCkpt)) {
    callback(null, 'sd ckpt is exist');
  } else {
    await downloads(fileUrl, {
      dest: downloadDir,
      filename,
      extract: false,
    });
    callback(null, 'download success');
  }
};
