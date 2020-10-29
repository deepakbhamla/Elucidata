import React from 'react';

import './App.css';
import { Upload, message, Button } from 'antd';
import { UploadOutlined } from '@ant-design/icons';

const props = {
  name: 'file',
  action: 'http://localhost:8000/upload/',
  headers: {
    authorization: 'authorization-text',
  },
  onChange(info) {
    if (info.file.status !== 'uploading') {
      console.log(info.file, info.fileList);
    }
    if (info.file.status === 'done') {
      message.success(`${info.file.name} file uploaded successfully`);
    } else if (info.file.status === 'error') {
      message.error(`${info.file.name} file upload failed.`);
    }
  },

  progress: {
    strokeColor: {
      '0%': 'red',
      '100%': 'orange',
    },
    strokeWidth: 5,
    format: percent => `${parseFloat(percent.toFixed(2))}%`,
  },
  };
  



const UploadFile = () => (
  <div className="App">
    <Upload {...props}>
       <Button icon={<UploadOutlined />} large>Click to Upload</Button>
    </Upload>,
  </div>
);

export default UploadFile;