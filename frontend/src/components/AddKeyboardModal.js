import React from 'react';

import {Modal, Button, Form, Input, Grid} from "semantic-ui-react";
import KeyboardWidget from "./KeyboardWidget";
import AddButtonModal from "./AddButtonModal";


class AddKeyboardModal extends React.Component {
    constructor(props) {
        super(props);

        let test_buttons = {
            buttons: [
                // {
                //     "text": "Hey",
                //     "url": "",
                //     "callback_data": "test"
                // }
            ]
        }

        this.state = {keyboard: null,
            buttons: test_buttons.buttons,
            showTriggerInputError: false,
            showImageField: false,
            showKeyboardField: false,
            showAddButtonModal: false,
        };

        this.toggleAddButtonModal = this.toggleAddButtonModal.bind(this);
        this.showAddButtonModal = this.showAddButtonModal.bind(this);
        this.hideAddButtonModal = this.hideAddButtonModal.bind(this);
        this.submitAddButtonModal = this.submitAddButtonModal.bind(this);
    }

    toggleAddButtonModal(state) {
        if (state === true) {
            this.setState({showAddButtonModal: true});
        } else if (state === false) {
            this.setState({showAddButtonModal: false});
        }
    }

    showAddButtonModal() {
        this.setState({showAddButtonModal: true});
    }
    hideAddButtonModal() {
        this.setState({showAddButtonModal: false});
    }

    submitAddButtonModal(data) {
        let button = {
            text: data.text,
            url: data.url,
            callback_data: data.callback_data
        }
        console.info(button);
        let joined = this.state.buttons.concat(button);
        console.info(joined)
        this.setState({buttons: joined})
        this.hideAddButtonModal();
    }

    render() {
        let submit_button;

        if (this.state.buttons.length <= 0) {
            submit_button = (
                <Button
                    content="Save"
                    labelPosition='right'
                    icon='checkmark'
                    disabled
                    // onClick={() => this.props.submitFunc(this.state)}
                    // positive
                    primary
                />
            )
        } else if (this.state.buttons.length > 0) {
            submit_button = (
                <Button
                    content="Save"
                    labelPosition='right'
                    icon='checkmark'
                    onClick={() => this.props.submitFunc(this.state)}
                    // positive
                    primary
                />
            )
        }

        return (
            <div>
                {this.state.showAddButtonModal && <AddButtonModal closeFunc={this.hideAddButtonModal} submitFunc={this.submitAddButtonModal}/>}

                <Modal open size={'small'}>
                <Modal.Header>Add keyboard</Modal.Header>
                <Modal.Content>
                    <KeyboardWidget buttons={this.state.buttons} addButtonClickHandler={this.showAddButtonModal} />
                    {/*<Grid columns={4}>*/}
                    {/*    <Grid.Row>*/}
                    {/*        <Grid.Column className="no-padding">*/}
                    {/*            <Button basic fluid>Click me</Button>*/}
                    {/*        </Grid.Column>*/}
                    {/*        <Grid.Column>*/}
                    {/*            <Button>Do mot</Button>*/}
                    {/*        </Grid.Column>*/}
                    {/*        <Grid.Column>*/}
                    {/*            <Button>Do mot</Button>*/}
                    {/*        </Grid.Column>*/}
                    {/*        <Grid.Column>*/}
                    {/*            <Button>Do mot</Button>*/}
                    {/*        </Grid.Column>*/}
                    {/*    </Grid.Row>*/}
                    {/*    <Grid.Row>*/}
                    {/*        <Grid.Column>*/}
                    {/*            <Button>Click me</Button>*/}
                    {/*        </Grid.Column>*/}
                    {/*        <Grid.Column>*/}
                    {/*            <Button fluid>Do mot</Button>*/}
                    {/*        </Grid.Column>*/}
                    {/*        <Grid.Column>*/}
                    {/*            <Button>Do mot</Button>*/}
                    {/*        </Grid.Column>*/}
                    {/*    </Grid.Row>*/}
                    {/*</Grid>*/}
                </Modal.Content>
                <Modal.Actions>
                    <Button color='black' onClick={this.props.closeFunc}>
                        Close
                    </Button>
                    {submit_button}
                </Modal.Actions>
            </Modal>
            </div>
        )
    }
}

export default AddKeyboardModal;
