import React from 'react';
import axios from 'axios'
import moment from 'moment';

class PlantTitle extends React.Component {
    constructor(props) {
        super(props);     
        this.state = {
            name: "",
            plantTime: "",
            time: ""
        };
    }
    
    componentDidMount() {
        axios.get('/back/getName').then(response => response.data)
            .then((data) => {
                this.setState({ name: data.name })
        })
        axios.get('/back/getPlantTime').then(response => response.data)
            .then((data) => {
                this.setState({ 
                    plantTime: moment.unix(data.time)
                })
            })
            .then(() => {
                this.setState({
                    time: this.state.plantTime.fromNow()
                })
            })
    }
    
    render() {
        return (
            <div className="App-plant-name">
                <u><h2>{this.state.name}'s Info</h2></u>
                <h3>{this.state.name} was planted {this.state.time}</h3>
            </div>
            
        );
    }
}

export default PlantTitle;