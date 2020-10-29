import React, { Component } from 'react'
import './App.css';
import { Card, Col, Row } from 'antd';
import { Button, Radio } from 'antd';
import { DownloadOutlined } from '@ant-design/icons';
import axios from 'axios'

export class Result extends Component {
    constructor(props) {
        super(props)
    
        this.state = {
                size: 'medium',
                isButtonClicked : false    
        }
    }
    

    handleDownload(data) {
        axios({
            url: `http://localhost:8000/upload/${data}`, //your url
            method: 'GET',
            responseType: 'blob', // important
          }).then((response) => {
             const url = window.URL.createObjectURL(new Blob([response.data]));
             const link = document.createElement('a');
             link.href = url;
             link.setAttribute('download', `${data}.xlsx`); //or any other extension
             document.body.appendChild(link);
             link.click();
             console.log(link)
          });
      }
    
    render() {
        const { size, isButtonClicked } = this.state;
        console.log(isButtonClicked)

        return (
            <div>
              <div className="site-card-wrapper" 
              style={{marginTop:"60px", backgroundColor:'#fafafa',padding:'20px',borderRadius:"2px", border:'1px dashed grey'}}>
            <Row gutter={16} style={{display:'flex'}}>
              <Col xl={8} style={{display:"flex",justifyContent:"center"}}>
                <Card title="LPC" bordered={false}>
                <Button type="primary" 
                    icon={<DownloadOutlined />} 
                    size={size} 
                    onClick= { (e) => this.handleDownload('lpc')}
                    >
                Download
                 </Button>

                </Card>
              </Col>
              <Col xl={8} style={{display:"flex",justifyContent:"center"}}>
                <Card title="PC" bordered={false} >
                <Button type="primary" 
                    icon={<DownloadOutlined />}  
                    size={size}
                    onClick= { (e) => this.handleDownload('pc')}
                    >
                      Download
                 </Button>

                </Card>
              </Col>
              <Col xl={8} style={{display:"flex",justifyContent:"center"}}>
                <Card title="PLASMALOGEN" bordered={false}>
                <Button type="primary" 
                    icon={<DownloadOutlined />} 
                    size={size}
                    onClick= { (e) => this.handleDownload('plasmalogen')}

                    >
                               Download
                 </Button>
                </Card>
              </Col>
            </Row>
          </div>  
          <div className="site-card-wrapper" 
              style={{marginTop:"60px", backgroundColor:'#fafafa',padding:'20px',borderRadius:"2px", border:'1px dashed grey'}}>
            <Row gutter={16} style={{display:'flex'}}>
              <Col xl={8} style={{display:"flex",justifyContent:"center"}}>
                <Card title="Retention Time Roundoff" bordered={false}>
                <Button type="primary" 
                    icon={<DownloadOutlined />} 
                    size={size} 
                    onClick= { (e) => this.handleDownload('roundoff')}
                    >
                Download
                 </Button>

                </Card>
              </Col>
              <Col xl={8} style={{display:"flex",justifyContent:"center"}}>
                <Card title="mean" bordered={false} >
                <Button type="primary" 
                    icon={<DownloadOutlined />}  
                    size={size}
                    onClick= { (e) => this.handleDownload('mean')}
                    >
                      Download
                 </Button>

                </Card>
              </Col>
            </Row>
          </div>  

          </div>     

        )
    }
}

export default Result
