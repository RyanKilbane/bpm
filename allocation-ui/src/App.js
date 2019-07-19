import React from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios';

function App() {
  var x = axios.get("http://localhost:5000/allocate")
  x.then(response => console.log(response.data))
  return x.then(response => response.data)
}

export default App;
