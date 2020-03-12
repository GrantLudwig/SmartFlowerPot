import React from 'react';
import axios from 'axios'

class MoistureLevel extends React.Component {
    constructor(props) {
        super(props);     
        this.state = {
            moist: ""
        };
    }
    
    componentDidMount() {
        axios.get('/back/moisture').then(response => response.data)
            .then((data) => {
                this.setState({ moist: data.moisture })
        })
    }
    
    render() {
        return (
            <div className="App-Moisture-Level">
                <h3>Moisture Level:</h3>
                <h4>{this.state.moist}%</h4>
            </div>
            
        );
    }
}

export default MoistureLevel;