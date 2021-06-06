import React from 'react';
import {BrowserRouter as Router, Route} from 'react-router-dom';

import './App.css';

import Navigation from "./components/Navigation";
import Dashboard from "./pages/Dashboard";
import Builder from "./pages/Builder";
import Stat from './pages/Stat';
import axios from "axios";
import Cookie from 'js-cookie';


class App extends React.Component {
    constructor(props) {
        super(props);

        console.log("[DEBUG] App constructor")

        let user_id = localStorage.getItem('user_id')
        this.state = {bot: undefined, user_id: user_id, validUser: false, password: ''}
    }

    componentDidMount() {
        console.log('app mounted')
        const csrftoken = Cookie.get('csrftoken');
        // axios.defaults.headers.common['X-CSRFToken'] = 'XMLHttpRequest';
        axios.defaults.headers.common['X-CSRFToken'] = csrftoken;
        console.log("[DEBUG] CSRFToken: ", csrftoken);
        window.p_url = 'https://docs.google.com/presentation/d/1icwHRx5HRxenKaI8-enVbBncDGEWzixOiL7NkqZvD5g/';
    }

    handlePassChange(event) {
        if (event.target.value == '10891089') {
            this.setState({validUser: true});
            window.localStorage.setItem('validUser', 'true');
        }
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
        })
    }

    render() {
        if (this.state.validUser == false && window.localStorage.getItem('validUser') == undefined) {
            return (
                <div>
                    <input type='password' onChange={event => {this.handlePassChange(event)}} />
                </div>
            )
        }

        if (this.state.user_id == null) {
            return (
                <div>
                    <h1>Not logged in</h1>
                    <button onClick={() => this.login()}>Login</button>
                </div>
            )
        }
        return (
            <Router>
                <Navigation />
                <Route path="/dashboard" component={() => <Dashboard user_id={this.state.user_id} />}/>
                <Route path='/builder' component={() => <Builder bot={this.state.bot} />} />
                <Route path='/stat' component={() => <Stat /> } />
            </Router>
        )
    }
}

export default App;
