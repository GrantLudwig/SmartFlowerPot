import React from 'react';
import axios from 'axios'

class IP extends React.Component {
    constructor(props) {
        super(props);     
        this.state = {
            ip: "",
            ssid: ""
        };
    }
    
    componentDidMount() {
        axios.get('/back/getNetwork').then(response => response.data)
            .then((data) => {
                this.setState({ ip: data.ip,
                                ssid: data.ssid})
        })
    }
    
    render() {
        return (
            <div className="App-ip">
                <p>To connect to site remotely on the {this.state.ssid} network: http://{this.state.ip}:5000</p>
            </div>
            
        );
    }
}

export default IP;