import React from 'react';
import axios from 'axios'

class WaterLevel extends React.Component {
    constructor(props) {
        super(props);     
        this.state = {
            waterLevel: ""
        };
    }
    
    componentDidMount() {
        axios.get('/back/waterLeft').then(response => response.data)
            .then((data) => {
                this.setState({ waterLevel: data.water })
        })
    }
    
    render() {
        return (
            <div className="App-Water-Level">
                <h3>Water Level:</h3>
                <h4>{this.state.waterLevel}%</h4>
            </div>
            
        );
    }
    
    updateLevel = () => {
        this.setState.waterLevel = "lol"
    }
}

export default WaterLevel;