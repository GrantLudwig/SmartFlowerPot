import React from 'react';
import axios from 'axios'

class LightOnTime extends React.Component {
    constructor(props) {
        super(props);     
        this.state = {
            time: ""
        };
    }
    
    componentDidMount() {
        axios.get('/back/light24').then(response => response.data)
            .then((data) => {
                this.setState({ time: data.time })
        })
    }
    
    render() {
        return (
            <div className="App-light-on">
                <h3>Yesterday's Light Usage:</h3>
                <h4>{this.state.time} min</h4>
            </div>
            
        );
    }
}

export default LightOnTime;