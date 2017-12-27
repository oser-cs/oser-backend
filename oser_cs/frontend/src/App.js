import React, {Component} from 'react';
import axios from 'axios';
import './App.css';


class App extends Component {
  constructor(props) {
    super(props)
    this.state = {text: 'Initial text!'}
  }
  render() {
    return (<div className="App">
      <button type="button" onClick={() => this.sendGET('http://localhost:8000/api/students/')}
        >Send GET /students
      </button>
      <button type="button" onClick={() => this.sendGET('http://localhost:8000/api/tutors/')}
        >Send GET /tutors
      </button>
      <button type="button" onClick={() => this.sendGET('http://localhost:8000/api/schools/')}
        >Send GET /schools
      </button>
      <p>{ this.state.text }</p>
    </div>);
  }

  sendGET(endpoint) {
    console.log("Sending a GET API Call !");
    axios.get(endpoint)
    .then(response => {
      this.setState({text: JSON.stringify(response.data)})
    })
  }
}

export default App;
