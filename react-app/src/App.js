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
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
    return (
        <div className="App">
            <h1>Smart Flower Pot</h1>
            <PlantTitle />
            <MoistureLevel></MoistureLevel>
            <LightLevel></LightLevel>
            <br />
            <h2>Flower Pot Info</h2>
            <WaterLevel></WaterLevel>
            <CurrentTemp></CurrentTemp>
            <LightOnTime></LightOnTime>
            <PlantSettings></PlantSettings>
        </div>
    );
}

export default App;
