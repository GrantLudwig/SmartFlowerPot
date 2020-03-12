import React from 'react';
import axios from 'axios'

class Test extends React.Component {
    constructor(props) {
        super(props);     
        this.state = {
            message: ""
        };
    }
    
    componentDidMount() {
        axios.get('/test').then(response => response.data)
            .then((data) => {
                this.setState({ message: data.thing })
        })
    }
    
    render() {
        return (
            <div className="App-test">
                <h3>
                    {this.state.message}
                </h3>
            </div>
            
        );
    }
}

export default Test;