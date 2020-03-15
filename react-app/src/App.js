import React from 'react';
import './App.css';
import axios from 'axios';
import Test from './test';
import LightOnTime from './LightOnTime';
import CurrentTemp from './CurrentTemp';
import WaterLevel from './WaterLevel';
import MoistureLevel from './MoistureLevel';
import LightLevel from './LightLevel';
import PlantSettings from './PlantSettings';
import PlantTitle from './PlantTitle';
import IP from './IP';
import 'bootstrap/dist/css/bootstrap.min.css';

class App extends React.Component {
    
    constructor(props) {
        super(props);
    }
    
    componentDidMount() {
        this.intervalID = setInterval(
            () => this.tick(),
            300000
        );
    }
    
    componentWillUnmount() {
        clearInterval(this.intervalID);
    }
    
    tick() {
        window.location.reload();
    }
    
    render() {
        return (
            <div className="App">
            <div className="App-header">
                <h1>Smart Flower Pot</h1>
                <PlantTitle />
                <MoistureLevel></MoistureLevel>
                <LightLevel></LightLevel>
                <br />
                <u><h2>Flower Pot Info</h2></u>
                <WaterLevel></WaterLevel>
                <CurrentTemp></CurrentTemp>
                <LightOnTime></LightOnTime>
                <PlantSettings></PlantSettings>
                <IP />
            </div>
            </div>
        );
    }
}

export default App;
