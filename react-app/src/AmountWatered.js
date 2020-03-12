import React from 'react';
import axios from 'axios'

class AmountWatered extends React.Component {
    constructor(props) {
        super(props);     
        this.state = {
            gallons: ""
        };
    }
    
    componentDidMount() {
        axios.get('/back/water24').then(response => response.data)
            .then((data) => {
                this.setState({ gallons: data.water })
        })
    }
    
    render() {
        return (
            <div className="App-amount-water">
                <h3>Water Used:</h3>
                <h4>{this.state.gallons} Gallons</h4>
            </div>
            
        );
    }
}

export default AmountWatered;