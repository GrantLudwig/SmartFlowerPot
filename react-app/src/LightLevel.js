import React from 'react';
import axios from 'axios'

class LightLevel extends React.Component {
    constructor(props) {
        super(props);     
        this.state = {
            light: ""
        };
    }
    
    componentDidMount() {
        axios.get('/back/light').then(response => response.data)
            .then((data) => {
                this.setState({ light: data.light })
        })
    }
    
    render() {
        return (
            <div className="App-Light-Level">
                <h3>Light Level:</h3>
                <h4>{this.state.light} Lux</h4>
            </div>
            
        );
    }
}

export default LightLevel;