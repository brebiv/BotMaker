import React from 'react';

import {Modal, Button, Form, Input} from "semantic-ui-react";
import AddKeyboardModal from "./AddKeyboardModal";


class AddModal extends React.Component {
    constructor(props) {
        super(props);

        this.state = {trigger: '', reply_text: '', image_url: '', keyboard: null,
            buttons: [],
            showTriggerInputError: false,
            showImageField: false,
            showKeyboardField: false,
            showKeyboardModal: false,
        };

        this.handleTriggerInputChange = this.handleTriggerInputChange.bind(this);
        this.handleReplyTextChange = this.handleReplyTextChange.bind(this);
        this.handleImageInputChange = this.handleImageInputChange.bind(this);
        this.addImageField = this.addImageField.bind(this);
        this.removeImageField = this.removeImageField.bind(this);
        this.addKeyboardField = this.addKeyboardField.bind(this);
        this.removeKeyboardField = this.removeKeyboardField.bind(this);
        this.showKeyboardModal = this.showKeyboardModal.bind(this);
        this.hideKeyboardModal = this.hideKeyboardModal.bind(this);
        this.submitKeyboardModal = this.submitKeyboardModal.bind(this);
    }

    handleTriggerInputChange(event) {
        let trigger_regex=/^[a-zA-Z0-9]+$/;

        if (trigger_regex.test(event.target.value)) {
            this.setState({trigger: event.target.value});
            this.setState({showTriggerInputError: false})
            console.log("TRUE")
        } else {
            this.setState({trigger: event.target.value});
            this.setState({showTriggerInputError: true})
            console.log("FALSE")
        }
    }

    handleImageInputChange(event) {
        this.setState({image_url: event.target.value});
    }

    handleReplyTextChange(event) {
        this.setState({reply_text: event.target.value});
    }

    addImageField() {
        this.setState({showImageField: true})
    }

    removeImageField() {
        this.setState({showImageField: false, image_url: ''})
    }

    addKeyboardField() {
        // console.log(this);
        this.setState({showKeyboardField: true});
    }

    removeKeyboardField() {
        this.setState({showKeyboardField: false, keyboard: null, buttons: []});
    }

    showKeyboardModal() {
        this.setState({showKeyboardModal: true});
    }

    hideKeyboardModal() {
        this.setState({showKeyboardModal: false});
    }

    submitKeyboardModal(data) {
        this.addKeyboardField();
        this.hideKeyboardModal();
        console.info(data);
        this.setState({buttons: data.buttons})
    }

    render() {

        let trigger_error_msg;
        if (this.state.showTriggerInputError) {
            trigger_error_msg = { content: 'MY ERROR', pointing: 'below' };
        }

        let submit_button;

        if (this.state.showTriggerInputError || this.state.reply_text === '') {
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
        } else if (!this.state.showTriggerInputError && this.state.reply_text !== '') {
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

        let image_field = '';

        if (this.state.showImageField) {
            image_field = (
                <Form.Field>
                    <label>Image url</label>
                    <Input type='url' defaultValue={this.state.image_url}  onChange={this.handleImageInputChange}/>
                </Form.Field>
            )
        }

        let keyboard_field = '';

        if (this.state.showKeyboardField) {
            keyboard_field = (
                <Form.Field>
                    <Button
                        content="Edit keyboard"
                        labelPosition='right'
                        icon='keyboard'
                        onClick={() => console.info("Soon")}
                        color='teal'
                        // secondary
                    />
                </Form.Field>
            )
        }

        let show_image_field_button = (
            <Button
                content="Add image"
                labelPosition='right'
                icon='image'
                onClick={this.addImageField}
                // positive
                primary
            />
        )

        let show_keyboard_field_button = (
            <Button
                content="Add keyboard"
                labelPosition='right'
                icon='keyboard'
                onClick={() => {
                    this.showKeyboardModal();
                }
                }
                // positive
                primary
            />
        )

        if (this.state.showImageField) {
            show_image_field_button = (<Button
                content="Remove image"
                labelPosition='right'
                icon='image'
                onClick={this.removeImageField}
                // positive
                primary
            />)
        }

        if (this.state.showKeyboardField) {
            show_keyboard_field_button = (
                <Button
                    content="Remove keyboard"
                    labelPosition='right'
                    icon='keyboard'
                    onClick={this.removeKeyboardField}
                    // positive
                    primary
                />
            )
        }

        return (
            <div>
                {this.state.showKeyboardModal && <AddKeyboardModal submitFunc={this.submitKeyboardModal} closeFunc={this.hideKeyboardModal}/>}
                <Modal open>
                <Modal.Header>Add</Modal.Header>
                <Modal.Content>
                    <Modal.Description>
                        <Form>
                            <Form.Field error={trigger_error_msg}>
                                <label>Trigger</label>
                                <Input type='text' label='/' defaultValue={this.state.commandWithoutSlash}  onChange={this.handleTriggerInputChange}/>
                            </Form.Field>
                            <Form.Field>
                                <label>Response</label>
                                <Input type='text' defaultValue={this.state.reply_text} onChange={this.handleReplyTextChange} />
                            </Form.Field>
                            {image_field}
                            {keyboard_field}
                            <Form.Field>
                                {show_image_field_button}
                                {show_keyboard_field_button}
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

export default AddModal;
