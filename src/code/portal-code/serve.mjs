import fs from 'fs-extra';
import crypto from 'crypto';
import path from 'path';
import express from 'express';
import process from 'process';
import ejs from 'ejs';
import { URL } from 'url';
import https from 'https';
import http from 'http';
import bodyParser from 'body-parser';

// import { createProxyMiddleware } from 'http-proxy-middleware';

import timeout from 'connect-timeout';
const app = express()
const port = 9000;


const CHATGLM2_6B_MODELS = [{
  name: 'pytorch_model-00001-of-00007.bin',
  sha256: 'cdf1bf57d519abe11043e9121314e76bc0934993e649a9e438a4b0894f4e6ee8'
}, {
  name: 'pytorch_model-00002-of-00007.bin',
  sha256: '1cd596bd15905248b20b755daf12a02a8fa963da09b59da7fdc896e17bfa518c'
}, {
  name: 'pytorch_model-00003-of-00007.bin',
  sha256: '812edc55c969d2ef82dcda8c275e379ef689761b13860da8ea7c1f3a475975c8'
}, {
  name: 'pytorch_model-00004-of-00007.bin',
  sha256: '555c17fac2d80e38ba332546dc759b6b7e07aee21e5d0d7826375b998e5aada3'
}, {
  name: 'pytorch_model-00005-of-00007.bin',
  sha256: 'cb85560ccfa77a9e4dd67a838c8d1eeb0071427fd8708e18be9c77224969ef48'
}, {
  name: 'pytorch_model-00006-of-00007.bin',
  sha256: '09ebd811227d992350b92b2c3491f677ae1f3c586b38abe95784fd2f7d23d5f2'
}, {
  name: 'pytorch_model-00007-of-00007.bin',
  sha256: '316e007bc727f3cbba432d29e1d3e35ac8ef8eb52df4db9f0609d091a43c69cb'
}];
const BASE_LLM_PATH = '/mnt/auto/llm'
const FC_MODEL_PATH = process.env.LLM_MODEL || '';

function calculateFileHash(filePath, algorithm = 'sha256') {
  return new Promise((resolve, reject) => {
    const hash = crypto.createHash(algorithm);
    const stream = fs.createReadStream(filePath);

    stream.on('data', (data) => hash.update(data));
    stream.on('end', () => resolve(hash.digest('hex')));
    stream.on('error', (error) => reject(error));
  });
}

function download(url, dest, res) {

  const filename = path.basename(url);
  const uri = new URL(url);
  const pkg = url.toLowerCase().startsWith('https:') ? https : http;
  pkg.get(uri.href).on('response', (_res) => {
    const len = parseInt(_res.headers['content-length'], 10);
    fs.ensureDirSync(dest);
    const filePath = path.join(dest, filename);
    if (_res.statusCode === 200) {
      const file = fs.createWriteStream(filePath);
      file.on('open', () => {
        let downloaded = 0;
        _res
          .on('data', (chunk) => {
            file.write(chunk);
            downloaded += chunk.length;
            res.write(`${JSON.stringify({
              total: len,
              currentSize: downloaded
            })}\n\n`);
          })
          .on('end', () => {
            res.write(`${JSON.stringify({
              total: len,
              currentSize: downloaded
            })}\n\n`);
            file.end();
            res.end();
          })
          .on('error', (err) => {
            file.destroy();
            fs.unlinkSync(dest);
          });
      });
    }
  });
}

app.use(bodyParser.json());

app.use(timeout('60s'));




app.set('views', process.cwd() + '/dist')
app.engine('html', ejs.renderFile)
app.set('view engine', 'ejs')


app.get('/', (req, res) => {
  res.render('index.html', {
    UID: req.get('x-fc-account-id'),
  })
});


app.delete('/model/:name', (req, res) => {
  const name = req.params.name;
  const filePath = path.join(BASE_LLM_PATH + '/' + FC_MODEL_PATH, name);
  const fileExist = fs.existsSync(filePath);
  if (fileExist) {
    fs.unlinkSync(filePath);
  }
  res.send('delete success');
});

app.get('/baseModel', (req, res) => {
  const baseModel = process.env.baseModel;
  res.send(baseModel);
});

app.get('/models', (req, res) => {
  const modelsStatusPromise = CHATGLM2_6B_MODELS.map((item) => {
    const name = item.name;
    const filePath = path.join(BASE_LLM_PATH + '/' + FC_MODEL_PATH, name);
    const fileData = { name, total: 1, currentSize: 0, downLoading: 0 };
    const fileExist = fs.existsSync(filePath);
    if (fileExist) {
      const stats = fs.statSync(filePath);
      const fileSizeInBytes = stats.size;
      fileData.total = fileSizeInBytes;
      fileData.currentSize = fileSizeInBytes;
    }
    return fileData;
  });

  res.json(modelsStatusPromise);
});


app.get('/modelReady', async (req, res) => {
  const checkHash = req.query.checkHash;
  let modelReady = true;

  if(process.env.LLM_MODEL === 'chatglm2-6b-int4') {
    res.send(modelReady);
    return;
  }
  for (const item of CHATGLM2_6B_MODELS) {
    const name = item.name;
    const sha256 = item.sha256;
    const filePath = path.join(BASE_LLM_PATH + '/' + FC_MODEL_PATH, name);
    const fileExist = fs.existsSync(filePath);
    if (!fileExist) {
      modelReady = '';
    } else if (checkHash) {
      const fileHash = await calculateFileHash(filePath);
      if (fileHash !== sha256) {
        modelReady = '';
      }
    }
  }

  res.send(modelReady);
})

app.get('/serverUrl', (req, res) => {
  const serverUrl = process.env.chatServerUrl || '';
  res.send(serverUrl);
});


app.get('/adminUrl', (req, res) => {
  const adminUrl = process.env.adminUrl || '';
  res.send(adminUrl);
});


app.post('/downloadModel', async (req, res) => {
  const modelName = req.body.modelName;
  const region = process.env.region || 'cn-hangzhou';
  const sourceFileUrl = `https://serverless-ai-models-${region}.oss-${region}-internal.aliyuncs.com/chatglm2-6b/${modelName}`;
  const filename = path.basename(sourceFileUrl);
  const chatglmModelFile = path.join(BASE_LLM_PATH + '/' + FC_MODEL_PATH, filename);
  const fileExist = fs.existsSync(chatglmModelFile);

  if (fileExist) {
    const currentModelItem = CHATGLM2_6B_MODELS.find((item) => item.name = modelName);
    const fileHash = await calculateFileHash(chatglmModelFile);
    if (fileHash === currentModelItem.sha256) {
      res.send('alreay exist');
      return;
    }
  }

  res.setHeader('Transfer-Encoding', 'chunked');
  res.setHeader('Content-type', 'text/event-stream;charset=utf-8');
  res.flushHeaders();

  download(sourceFileUrl, BASE_LLM_PATH + '/' + FC_MODEL_PATH, res);

});

app.use(express.static('dist'));

app.listen(port, () => {
  console.log(`web app listening on port ${port}`)
})