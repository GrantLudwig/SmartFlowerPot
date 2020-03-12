import React from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import Test from './test';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <p>My Token = {window.token}</p>
        <Test></Test>
      </header>
    </div>
  );
}

export default App;
