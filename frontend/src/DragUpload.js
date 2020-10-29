import React from 'react';
import { Upload, message } from 'antd';
import { InboxOutlined } from '@ant-design/icons';
import './App.css'
import './drag.css'

const { Dragger } = Upload;

const props = {
  name: 'file',
  multiple: true,
  action: 'http://localhost:8000/upload/excelFile/',
  onChange(info) {
    const { status } = info.file;
    if (status !== 'uploading') {
      console.log(info.file, info.fileList);
    }
    if (status === 'done') {
      message.success(`${info.file.name} file uploaded successfully.`);
    } else if (status === 'error') {
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
const DragUpload = () => (
    <div className="App">
  
  <Dragger {...props}>
    <p className="ant-upload-drag-icon">
      <InboxOutlined />
    </p>
    <p className="ant-upload-text">Click or drag file to this area to upload</p>
    <p className="ant-upload-hint">
      please uploads only excel(.xlsx) file otherwise it give error
    </p>
  </Dragger>
  </div>
  )
export default DragUpload