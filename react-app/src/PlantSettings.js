import React from 'react';
import axios from 'axios';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import ModalDialog from 'react-bootstrap/ModalDialog';
import ModalHeader from 'react-bootstrap/ModalHeader';
import ModalTitle from 'react-bootstrap/ModalTitle';
import ModalBody from 'react-bootstrap/ModalBody';
import ModalFooter from 'react-bootstrap/ModalFooter';
import Form from 'react-bootstrap/Form';
import Overlay from 'react-bootstrap/Overlay';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import 'bootstrap/dist/css/bootstrap.min.css';

class PlantSettings extends React.Component {
    constructor(props) {
        super(props);     
        this.state = {
            name: "",
            type: ""
        }; 
    }
    
    componentDidMount() {
        axios.get('/back/getType').then(response => response.data)
            .then((data) => {
                this.setState({ type: data.type })
        })
    }
    
    render() {
        return (
            <div>
                <br />
                <WaterFilled />
                <Popup name={this.state.name} type={this.state.type}/>
            </div> 
        );
    }
}

function WaterFilled() {
    const handlePress = () => axios.put('/back/resetWater').then(() => 
        this.Obj.updateLevel()
    );
    const refresh = () => window.location.reload();
    return (
        <>
            <OverlayTrigger
                placement="right"
                delay={{ show: 250, hide: 400 }}
                overlay={renderTooltip}
            >
                <Button variant="primary" size="lg" onClick={() => {handlePress(); refresh();}} block>
                    Water Filled
                </Button>
            </OverlayTrigger>
        </>
    );
}

function Popup(props) {        
    const [show, setShow] = React.useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    const resetPlant = () =>
        axios.post('/back/newPlant', {
            name: props.name,
            type: props.type
        })
        .then(function (response) {
            console.log(response);
        })
        .catch(function (error) {
            console.log(error);
    });
    const refresh = () => window.location.reload();
    const handleNameChange = (e) => props.name = e.target.value;
    const handleTypeChange = (e) => props.type = e.target.value;

    return (
        <>
            <Button variant="success" size="lg" onClick={handleShow} block>
                Change Plant
            </Button>

            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>New Plant</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        <Form.Group controlId="plantChoice">
                            <Form.Label>Plant Type</Form.Label>
                            <Form.Control as="select" onChange={handleTypeChange}>
                                <option>Basil</option>
                                <option>Cilantro</option>
                                <option>Rosemary</option>
                            </Form.Control>
                        </Form.Group>
                        <Form.Group controlId="plantName">
                            <Form.Label>Plant Name</Form.Label>
                            <Form.Control type="text" placeholder="Name" onChange={handleNameChange}/>
                        </Form.Group>
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleClose}>
                        Close
                    </Button>
                    <OverlayTrigger
                        placement="right"
                        delay={{ show: 250, hide: 400 }}
                        overlay={renderTooltipPlant}
                    >
                        <Button variant="primary" onClick={() => {resetPlant(); handleClose(); refresh();}}>
                            Save New Plant
                        </Button>
                    </OverlayTrigger>
                </Modal.Footer>
            </Modal>
        </>
    );
}

function renderTooltipPlant(props) {
  return <Tooltip {...props}>Will setup a new plant</Tooltip>;
}

function renderTooltip(props) {
  return <Tooltip {...props}>Will reset the water level to full</Tooltip>;
}

export default PlantSettings;