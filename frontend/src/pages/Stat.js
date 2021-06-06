import React from 'react';

import axios from "axios";

import BotStatusCard from "../components/BotStatusCard";
import {Button, Segment, Card, Image} from "semantic-ui-react";



class Stat extends React.Component {
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
            numberOfTodayUsers: 0
        }

        this.getMessages = this.getTodayMessages.bind(this);
    }

    componentDidMount() {
        this.getTodayMessages();
    }

    getTodayMessages() {
        axios.get(`/api/v1/bots/${this.state.bot_id}/messages?date=today`).then(resp => {
            window.messages = resp.data;
            let messages = resp.data;
            let users = [];
            messages.forEach(message => {
                if (!users.includes(message.sender_tid)) {
                    users.push(message.sender_tid);
                }
            });
            this.setState({messages: resp.data, numberOfTodayUsers: users.length});
            console.log(resp.data);
        })
    }

    getAllMessages() {
        axios.get(`/api/v1/bots/${this.state.bot_id}/messages`).then(resp => {

        })
    }

    render() {
        return(
            <main>
                <Segment compact secondary>
                    <h1>Statistics</h1>
                </Segment>
                <Card color="red">
                    <Card.Content>
                        <Card.Header>Statistics</Card.Header>
                    </Card.Content>
                    <Card.Content id="bot-status-card">
                        <h5>Today received: {this.state.messages.length} messages</h5>
                        <h5>Today users: {this.state.numberOfTodayUsers}</h5>
                    </Card.Content>
                    <Card.Content extra>
                        Conclusion: You're doing fine
                    </Card.Content>
                </Card>
                <Card color="red">
                    <Card.Content>
                        <Card.Header>Statistics</Card.Header>
                    </Card.Content>
                    <Card.Content id="bot-status-card">
                        <Image src="/interactive-line-graph.png" />
                    </Card.Content>
                    <Card.Content extra>
                        Graph says everything is going great
                    </Card.Content>
                </Card>
            </main>
        )
    }
}

export default Stat;
