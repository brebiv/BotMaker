import React from 'react';

import axios from "axios";

import {Segment, Table, List, Button, Grid, Icon, Divider} from "semantic-ui-react";
import EditModal from "../components/EditModal";

import './Builder.css';
import AddModal from "../components/AddModal";
import AddCallbackModal from "../components/AddCallbackModal";
import EditCallbackModal from "../components/EditCallbackModal";
import Cookie from "js-cookie";


class Builder extends React.Component {
    constructor(props) {
        super(props);

        let user_id = localStorage.getItem('user_id');
        let bot_id = localStorage.getItem('bot_id');

        this.state = {
            bot: undefined,
            bot_id: bot_id,
            user_id: user_id,
            commands: [],
            callbacks: [],
            callback_datas: [],
            loading: true,
            showEditModal: false,
            editId: undefined,
            showAddModal: false,
            showAddCallbackModal: false,
            showEditCallbackModal: false
        }

        this.getCommands = this.getCommands.bind(this);
        this.getCallbacks = this.getCallbacks.bind(this);
        this.submitEditModal = this.submitEditModal.bind(this);
        this.closeEditModal = this.closeEditModal.bind(this);
        this.submitAddModal = this.submitAddModal.bind(this);
        this.closeAddModal = this.closeAddModal.bind(this);
        this.submitAddCallbackModal = this.submitAddCallbackModal.bind(this);
        this.closeAddCallbackModal = this.closeAddCallbackModal.bind(this);
        this.addCommand = this.addCommand.bind(this);
        this.addCallbackHandler = this.addCallbackHandler.bind(this);
        this.deleteCommand = this.deleteCommand.bind(this);
    }

    componentDidMount() {
        this.getCommands();
        this.getCallbacks();

        if (this.state.user_id != null) {
            let csrf_token = Cookie.get('csrftoken')
            console.info("[DEBUG] Got csrf from cookie:", csrf_token)
            axios.defaults.headers.common['X-CSRFToken'] = csrf_token;
        }
    }

    getCommands() {
        axios.get(`api/v1/bots/${this.state.bot_id}/commands/`).then(resp => {
            console.info("[DEBUG] getCommands resp data:", resp.data)
            this.setState({commands: resp.data})
            let callback_datas = [];
            resp.data.forEach(command => {
                command.buttons.forEach(button => {
                    callback_datas.push(button.callback_data);
                })
            });
            this.setState({callback_datas: callback_datas});
            console.log("Callback datas", callback_datas);
        })
    }

    getCallbacks() {
        axios.get(`api/v1/bots/${this.state.bot_id}/callbacks`).then(resp => {
            console.info("[DEBUG] getCallbacks resp data:", resp.data)
            this.setState({callbacks: resp.data});
        })
    }

    getInlineKeyboardButtons(command_id) {
        axios.get(`api/v1/commands/${command_id}/inline_buttons/`).then(data => {
            console.log("DATA", data);
        })
    }

    handleEditCommandClick(command) {
        // axios.post()
        console.log("[DEBUG] Command to edit:". command)
        // console.log(command)
        this.setState({editCommand: command, showEditModal: true})
    }

    handleEditCallbackClick(callback) {
        console.log("[DEBUG] Callback to edit:", callback);
        this.setState({editCallback: callback, showEditCallbackModal: true});
    }

    addCommand(command) {
        axios.post(`api/v1/bots/${this.state.bot_id}/commands/`, {
            trigger: '/' + command.trigger,
            reply_text: command.reply_text,
            reply_img_url: command.image_url,
            buttons: command.buttons,
            bot_id: this.state.bot_id,
            owner_id: this.state.user_id,
        }).then(resp => {
            let joined = this.state.commands.concat(resp.data);
            console.info(joined);
            this.setState({commands: joined});
        })
    }

    editCommand(command) {
        axios.put(`api/v1/commands/${command.id}/`, command).then(resp => {
            window.location.reload();
        })
    }

    // editCallback(callback) {
    //     axios.put
    // }

    deleteCommand(command) {
        console.log("[DEBUG] Delete command");
        console.log(command);
        axios.delete(`api/v1/commands/${command.command.id}/`).then(resp => {
            this.getCommands();
            this.setState({showEditModal: false});
        })
    }

    deleteCallback(callback) {
        console.log("[DEBUG] Delete callback", callback);
        axios.delete(`api/v1/callbacks/${callback.id}`).then(resp => {
            this.getCallbacks();
            this.setState({showEditCallbackModal: false});
        })
    }

    submitEditModal(data) {
        console.log("[DEBUG] Submit edit modal")
        this.setState({showEditModal: false});
        console.log(data);
        this.editCommand(data.command);
    }

    closeEditModal() {
        console.log("[DEBUG] Close edit modal");
        this.setState({showEditModal: false});
    }

    submitAddModal(data) {
        console.log("[DEBUG] Submit add modal")
        this.setState({showAddModal: false});
        console.log(data)
        this.addCommand(data);
    }

    submitAddCallbackModal(data) {
        console.log("[DEBUG] Submit add callback modal");
        this.setState({showAddCallbackModal: false});
        this.addCallbackHandler(data);
    }

    closeAddModal() {
        this.setState({showAddModal: false});
    }
    
    addCallbackHandler(callback_handler) {
        axios.post(`api/v1/bots/${this.state.bot_id}/callbacks/`, {
            trigger: callback_handler.trigger,
            reply_text: callback_handler.reply_text,
            reply_img_url: callback_handler.image_url,
            bot_id: this.state.bot_id
        })
    }

    closeAddCallbackModal() {
        this.setState({showAddCallbackModal: false});
    }

    render() {

        let command_rows = []
        let callback_rows = []

        this.state.commands.forEach(bot_command => {

            command_rows.push((
                <List.Item>
                    {/*<Icon name='help' />*/}
                    <List.Content floated='right'>
                        <Button onClick={()=>this.handleEditCommandClick(bot_command)}>Edit</Button>
                    </List.Content>
                    <List.Content>
                        <h4>{bot_command.trigger}</h4>
                    </List.Content>
                </List.Item>
            ))
        })

        this.state.callbacks.forEach(callback => {
            callback_rows.push((
                <List.Item>
                    {/*<Icon name='help' />*/}
                    <List.Content floated='right'>
                        <Button onClick={()=>this.handleEditCallbackClick(callback)}>Edit</Button>
                    </List.Content>
                    <List.Content>
                        <h4>{callback.trigger}</h4>
                    </List.Content>
                </List.Item>
            ))
        })

        // if (command_rows.length < 0) {
        //     command_rows = <h2>Loading</h2>
        // }

        return(
            <main>
                {this.state.showEditModal && <EditModal submitFunc={this.submitEditModal} closeFunc={this.closeEditModal} deleteCommandFunc={this.deleteCommand} editable={this.state.editCommand} />}
                {this.state.showAddModal && <AddModal submitFunc={this.submitAddModal} closeFunc={this.closeAddModal} />}
                {this.state.showAddCallbackModal && <AddCallbackModal submitFunc={this.submitAddCallbackModal} closeFunc={this.closeAddCallbackModal} callback_datas={this.state.callback_datas} />}
                {this.state.showEditCallbackModal && <EditCallbackModal closeFunc={()=>this.setState({showEditCallbackModal: false})} deleteFunc={(callback)=>this.deleteCallback(callback)} editable={this.state.editCallback} />}

                <Segment compact secondary>
                    <h1>Builder</h1>
                    {/*<Button onClick={() => this.login()}>Login</Button>*/}
                    {/*<Button onClick={() => this.logout()}>Logout</Button>*/}
                </Segment>
                <Grid columns={2} relaxed='very' id="builder-grid">
                    <Grid.Column class="builder-column">
                        <Segment secondary attached="top">
                            <h4>Commands</h4>
                        </Segment>
                        <Segment attached>
                            <List divided verticalAlign='middle' className="scrolling-list">
                                {this.state.commands.length > 0
                                    ? command_rows
                                    : <h2>No commands</h2>}
                                {/*{command_rows}*/}
                            </List>
                        </Segment>
                        <Segment secondary clearing attached="bottom">
                            <Button
                                floated='right'
                                icon
                                labelPosition='left'
                                primary
                                size='small'
                                onClick={() => this.setState({showAddModal: true})}
                            >
                                <Icon name='add' />Add
                            </Button>
                        </Segment>
                    </Grid.Column>

                    {/* CALLBACKS */}
                    <Grid.Column>
                        <Segment secondary attached="top">
                            <h4>Callbacks</h4>
                        </Segment>
                        <Segment attached>
                            <List divided verticalAlign='middle' className="scrolling-list">
                                {this.state.callbacks.length > 0
                                    ? callback_rows
                                    : <h2>No callbacks</h2>}
                            </List>
                        </Segment>
                        <Segment secondary clearing attached="bottom">
                            <Button
                                floated='right'
                                icon
                                labelPosition='left'
                                primary
                                size='small'
                                onClick={() => this.setState({showAddCallbackModal: true})}
                            >
                                <Icon name='add' />Add
                            </Button>
                        </Segment>
                    </Grid.Column>
                </Grid>
            </main>
        )

    }
}

export default Builder;
