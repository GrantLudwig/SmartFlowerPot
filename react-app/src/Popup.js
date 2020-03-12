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
import WaterLevel from './WaterLevel';
import 'bootstrap/dist/css/bootstrap.min.css';

class Popup extends React.Component {
    constructor(props) {
        super(props);     
        this.state = {
            name: "",
            type: "",
            [show, setShow] = React.useState(false)
        }; 
    }
    
    handleShow() {
        this.setShow(false);
    }
    
    handleShow() {
        this.setShow(true);
    }
    
    resetPlant() {
        axios.post('/back/newPlant', {
            name: newName.value,
            type: 'Basil'
        })
        .then(function (response) {
            console.log(response);
        })
        .catch(function (error) {
            console.log(error);
        });
    }
    
    refresh() {
        window.location.reload();
    }
    
    render() {
        return (
            <div>
                <Button variant="success" onClick={this.handleShow}>
                Change Plant
            </Button>

            <Modal show={show} onHide={this.handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>New Plant</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        <Form.Group controlId="plantChoice">
                            <Form.Label>Plant Type</Form.Label>
                            <Form.Control as="select">
                                <option>Basil</option>
                                <option>Cilantro</option>
                                <option>Rosemary</option>
                            </Form.Control>
                        </Form.Group>
                        <Form.Group controlId="plantName">
                            <Form.Label>Plant Name</Form.Label>
                            <Form.Control type="text" placeholder="Name"}/>
                        </Form.Group>
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={this.handleClose}>
                        Close
                    </Button>
                    <OverlayTrigger
                        placement="right"
                        delay={{ show: 250, hide: 400 }}
                        overlay={renderTooltipPlant}
                    >
                        <Button variant="primary" onClick={() => {this.resetPlant(); this.handleClose(); this.refresh();}}>
                            Save New Plant
                        </Button>
                    </OverlayTrigger>
                </Modal.Footer>
            </Modal>
            </div> 
        );
    }
}

function renderTooltipPlant(props) {
  return <Tooltip {...props}>Will setup a new plant</Tooltip>;
}

function renderTooltip(props) {
  return <Tooltip {...props}>Will reset the water level to full</Tooltip>;
}

export default Popup;