import React, { Component } from 'react';
import RipenessModule from "./components/ripeness_module"

export default class Home extends Component {
  render() {
    return (
      <div className="App">
        <h1>Banana Ripeness Detector</h1>
        <RipenessModule/>
      </div>
    );
  }
}


