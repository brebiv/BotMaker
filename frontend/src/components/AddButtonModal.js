import React from 'react';

import {Modal, Button, Form, Input, Label, Container} from "semantic-ui-react";


class AddButtonModal extends React.Component {
    constructor(props) {
        super(props);

        this.state = {text: '', url: '', callback_data: ''};

        this.handleButtonTextChange = this.handleButtonTextChange.bind(this);
        this.handleUrlChange = this.handleUrlChange.bind(this);
        this.handleCallbackDataChange = this.handleCallbackDataChange.bind(this);
    }

    handleButtonTextChange(event) {
        this.setState({text: event.target.value});
    }
    handleUrlChange(event) {
        this.setState({url: event.target.value});
    }
    handleCallbackDataChange(event) {
        this.setState({callback_data: event.target.value});
    }

    render() {

        let trigger_error_msg;
        if (this.state.showTriggerInputError) {
            trigger_error_msg = { content: 'MY ERROR', pointing: 'below' };
        }

        let submit_button;

        if (this.state.text === '' || this.state.callback_data === '') {
            submit_button = (
                <Button
                    content="Add"
                    labelPosition='right'
                    icon='checkmark'
                    disabled
                    // positive
                    primary
                />
            )
        } else {
            submit_button = (
                <Button
                    content="Add"
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
                <Modal open size={'small'}>
                    <Modal.Header>Add button</Modal.Header>
                    <Modal.Content>
                        <Modal.Description>
                            <Form>
                                <Form.Field error={trigger_error_msg}>
                                    <label>Button text</label>
                                    <Input type='text' onChange={this.handleButtonTextChange}/>
                                </Form.Field>
                                <Form.Field>
                                    <label>URL<Label style={{marginLeft: '1rem'}} color='purple'>Optional</Label></label>
                                    <Input type='url' onChange={this.handleUrlChange} />
                                </Form.Field>
                                <Form.Field>
                                    <label>Callback data</label>
                                    <Input type='text' onChange={this.handleCallbackDataChange} />
                                </Form.Field>
                                {/*{image_field}*/}
                                {/*{keyboard_field}*/}
                                <Form.Field>
                                    {/*{show_image_field_button}*/}
                                    {/*{show_keyboard_field_button}*/}
                                </Form.Field>
                            </Form>
                        </Modal.Description>
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

export default AddButtonModal;
