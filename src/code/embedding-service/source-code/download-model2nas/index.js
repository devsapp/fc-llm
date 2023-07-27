'use strict';
const path = require('path');
const fs = require('fs');
const downloads = require('@serverless-devs/downloads').default;

exports.handler = async (_event, _context, callback) => {
  const region = process.env.region || 'cn-hangzhou';
  const fileUrl = `https://serverless-ai-models-${region}.oss-cn-hangzhou-internal.aliyuncs.com/text2vec-large-chinese/pytorch_model.bin`;
  const filename = path.basename(fileUrl);
  const downloadDir = '/mnt/auto/embedding/text2vec-large-chinese';
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
