import React, { Component } from 'react';
import RipenessModule from "./components/ripeness_module"
// import './home.css'

const h1Style = {
  fontSize: '5em',
  color: '#ED9E46',
  fontFamily: 'Montserrat',
  marginTop: '25px'
};

const spanStyle = {
  color: '#666666'
};

export default class Home extends Component {
  render() {
    return (
      <div className="App">
        <h1 style={h1Style}>Banana <span style={spanStyle}>Ripeness</span></h1>
        <RipenessModule/>
      </div>
    );
  }
}


