import React from 'react';
import axios from 'axios'

class CurrentTemp extends React.Component {
    constructor(props) {
        super(props);     
        this.state = {
            temp: ""
        };
    }
    
    componentDidMount() {
        axios.get('/back/temp').then(response => response.data)
            .then((data) => {
                this.setState({ temp: data.temp })
        })
    }
    
    render() {
        return (
            <div className="App-temp">
                <h3>Current Temperature:</h3>
                <h4>{this.state.temp} fahrenheit</h4>
            </div>
            
        );
    }
}

export default CurrentTemp;