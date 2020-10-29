import React from 'react';
import './App.css';
import UploadFile from './upload'
import DragUpload from './DragUpload'
import Result from './Result'

import Logo from'./logo.svg';
import { Layout, Menu } from 'antd';

import {
  MenuUnfoldOutlined,
  MenuFoldOutlined,
  UserOutlined,
  VideoCameraOutlined,
  UploadOutlined,
  SolutionOutlined,
  BookOutlined
} from '@ant-design/icons';

const { Header, Sider, Content } = Layout;

class App extends React.Component {
  state = {
    collapsed: false,
  };

  toggle = () => {
    this.setState({
      collapsed: !this.state.collapsed,
    });
  };

  render() {
    return (
      <Layout>
        <Sider trigger={null} collapsible collapsed={this.state.collapsed}>
          <div className="logo" style={{width:'100%', display:"flex",justifyContent:"cennter",padding:"5px",backgroundColor:'#fff'}} >
            <img src='https://media-exp1.licdn.com/dms/image/C4D0BAQFvV6wEsL8a9g/company-logo_200_200/0?e=1611792000&v=beta&t=0pQ-QrST3D5mHYNYHPDgcm1CkSzBoAP65xxo78f4S-o' style={{width:"52px",margin:"auto"}} />
          </div>
          <Menu theme="dark" mode="inline" defaultSelectedKeys={['1']}>
            <Menu.Item key="1" icon={<SolutionOutlined />}>
              Assignment
            </Menu.Item>
            <Menu.Item key="2" icon={<BookOutlined/>}>
            Documentation
            </Menu.Item>
            <Menu.Item key="3" icon={<UserOutlined />}>
              About me
            </Menu.Item>
          </Menu>
        </Sider>
        <Layout className="site-layout">
          <Header className="site-layout-background" style={{ padding: '0',backgrounColor:"#fff" }}>
            {React.createElement(this.state.collapsed ? MenuUnfoldOutlined : MenuFoldOutlined, {
              className: 'trigger',
              onClick: this.toggle,
            })}
          </Header>
          <Content
            className="site-layout-background"
            style={{
              margin: '24px 16px',
              padding: 24,
              minHeight: 620,
            }}
          >
            <div className='box'>
               <DragUpload/>
               <Result/>
            </div>
          </Content>
        </Layout>
      </Layout>
    );
  }
}

export default App;