import React from 'react';

import {Modal, Button, Header, Input, Form} from "semantic-ui-react";


class EditModal extends React.Component {
    constructor(props) {
        super(props);

        let trigger = props.editable.trigger;
        let reply_text = props.editable.reply_text;
        let command_without_slash = trigger.slice(1);

        this.state = {
            commandWithoutSlash: command_without_slash,
            trigger: trigger,
            reply_text: reply_text,
            command: props.editable,
        };

        this.handleTriggerInputChange = this.handleTriggerInputChange.bind(this);
        this.handleReplyTextChange = this.handleReplyTextChange.bind(this);
        this.handleImageInputChange = this.handleImageInputChange.bind(this);
    }

    handleTriggerInputChange(event) {
        let c = this.state.command;
        c.trigger = '/' + event.target.value;
        this.setState({command: c});
    }

    handleReplyTextChange(event) {
        let c = this.state.command;
        c.reply_text = event.target.value;
        this.setState({command: c});
    }
    
    handleImageInputChange(event) {
        let c = this.state.command;
        c.reply_img_url = event.target.value;
        this.setState({command: c});
    }

    render() {

        let image_field = '';

        if (this.state.command.reply_img_url) {
            image_field = (
                <Form.Field>
                    <label>Image url</label>
                    <Input type='url' defaultValue={this.state.command.reply_img_url}  onChange={this.handleImageInputChange}/>
                </Form.Field>
            )
        } 

        return (
            <Modal open>
                <Modal.Header>Edit</Modal.Header>
                <Modal.Content>
                    <Modal.Description>
                        {/*<Input type='text' label='Trigger' defaultValue={this.props.editable.trigger} />*/}
                        <Form>
                            <Form.Field>
                                <label>Trigger</label>
                                <Input type='text' label='/' defaultValue={this.state.commandWithoutSlash}  onChange={this.handleTriggerInputChange}/>
                            </Form.Field>
                            <Form.Field>
                                <label>Response</label>
                                <Input type='text' defaultValue={this.state.reply_text} onChange={this.handleReplyTextChange} />
                            </Form.Field>
                            {image_field}
                        </Form>
                    </Modal.Description>
                </Modal.Content>
                <Modal.Actions>
                    <Button
                        content="Delete"
                        onClick={() => this.props.deleteCommandFunc(this.state)}
                        // positive
                        color='red'
                        floated='left'
                    />
                    <Button color='black' onClick={this.props.closeFunc}>
                        Close
                    </Button>
                    <Button
                        content="Change"
                        onClick={() => this.props.submitFunc(this.state)}
                        // positive
                        primary
                    />
                </Modal.Actions>
            </Modal>
        )
    }
}

export default EditModal;
