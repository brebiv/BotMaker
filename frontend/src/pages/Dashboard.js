import React from 'react';

import axios from "axios";

import './Dashboard.css'
import BotStatusCard from "../components/BotStatusCard";
import {Button, Segment} from "semantic-ui-react";


class Dashboard extends React.Component {
    constructor(props) {
        super(props);

        let user_id = localStorage.getItem('user_id');
        let bot_id = localStorage.getItem('bot_id');

        this.state = {
            bot: {},
            loading: true,
            user_id: user_id,
            bot_id: bot_id,
            messages: [],
        }

        this.startBot = this.startBot.bind(this);
        this.stopBot = this.stopBot.bind(this);
        this.getMessages = this.getMessages.bind(this);
    }

    componentDidMount() {
        axios.get(`/api/v1/bots/${this.state.bot_id}/`).then(res => {
            console.log(res.data)
            this.setState({bot: res.data, loading: false})
        })
        this.getMessages();
    }

    startBot() {
        axios.get(`/api/v1/bots/${this.state.bot_id}/start/`).then(res => {
            console.log(res.data)
            this.setState({bot: res.data})
        })
    }

    stopBot() {
        axios.get(`/api/v1/bots/${this.state.bot_id}/stop/`).then(res => {
            this.setState({bot: res.data})
        })
    }

    getMessages() {
        axios.get(`/api/v1/bots/${this.state.bot_id}/messages?date=today`).then(resp => {
            window.messages = resp.data;
            this.setState({messages: resp.data});
            console.log(resp.data);
        })
    }

    login() {
        axios.post('/api/v1/login/', {
            email: 'brebiv@gmail.com',
            password: '10891089'
        }).then(resp => {
            localStorage.setItem('user_id', resp.data.user_id);
            localStorage.setItem('bot_id', resp.data.bot_id);
            document.location.href = '/dashboard';
        })
    }

    logout() {
        axios.get('/api/v1/logout/').then(resp => {
            console.log(resp.data)
            localStorage.removeItem('user_id');
            localStorage.removeItem('bot_id');
            document.location.href = '/';
        })
    }

    render() {
        return(
            <main>
                <Segment compact secondary>
                    <h1>Dashboard</h1>
                    {/*<Button onClick={() => this.login()}>Login</Button>*/}
                    <Button onClick={() => this.logout()}>Logout</Button>
                </Segment>
                {this.state.loading
                    ? <h1>Loading</h1>
                    : <BotStatusCard bot={this.state.bot} startBotFunc={this.startBot} stopBotFunc={this.stopBot} bot_id={this.state.bot_id} />
                }
            </main>
        )
    }
}

export default Dashboard;
