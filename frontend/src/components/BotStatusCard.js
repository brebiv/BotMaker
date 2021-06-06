import React from 'react';
import {Button, Card, Segment} from "semantic-ui-react";

import axios from "axios";


class BotStatusCard extends React.Component {
    constructor(props) {
        super(props);

        this.state = {bot_id: props.bot_id, messages: [], numberOfTodayUsers: 0}

        this.getMessages = this.getMessages.bind(this);
        // setInterval(this.getNumberOfTodayMessages, 3000);
    }

    componentDidMount() {
        this.getMessages();
    }

    getMessages() {
        axios.get(`/api/v1/bots/${this.state.bot_id}/messages?date=today`).then(resp => {
            window.messages = resp.data;
            this.setState({messages: resp.data});
            console.log(resp.data);
        })
    }

    render() {
        let bot_status_row;
        let start_stop_button;

        if (this.props.bot.status === 0) {
            bot_status_row = (
                <div className="bot-status-row">
                    <h4>Stopped</h4>
                    <span className='red-ball'></span>
                </div>
            )

            start_stop_button = (
                <Button fluid color='green' onClick={this.props.startBotFunc}>
                    Start
                </Button>
            )
        } else if (this.props.bot.status === 1) {
            bot_status_row = (
                <div className="bot-status-row">
                    <h4>Running</h4>
                    <span className='ok-ball'></span>
                </div>
            )

            start_stop_button = (
                <Button fluid color='red' onClick={this.props.stopBotFunc}>
                    Stop
                </Button>
            )
        }

        return (
            <Card color="red">
                <Card.Content>
                    <Card.Header>{this.props.bot.username} status</Card.Header>
                </Card.Content>
                <Card.Content id="bot-status-card">
                    {bot_status_row}
                    <h5>Today received: {this.state.messages.length} messages</h5>
                    {/* <h5>Today users: {this.state.numberOfTodayUsers}</h5> */}
                </Card.Content>
                <Card.Content extra>
                    {start_stop_button}
                </Card.Content>
            </Card>
        )
    }
}

export default BotStatusCard;
