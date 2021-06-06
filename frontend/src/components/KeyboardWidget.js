import React from 'react';
import './keyboard.css';

class KeyboardWidget extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            buttons: props.buttons,
            showAddButtonModal: false,
        }
    }

    componentDidUpdate(prevProps) {
        // For re-rendering every time props change
        if(prevProps.buttons !== this.props.buttons) {
            this.setState({buttons: this.props.buttons});
        }
    }

    render() {
        let buttons_elements = [];

        this.state.buttons.forEach(button => {
            buttons_elements.push((
                <div className="keyboard-button">
                    <p className="button-text">{button.text}</p>
                </div>
            ))
        })

        return (
            <div className="keyboard-wrapper">
                <div className="keyboard-selector">
                    {buttons_elements}
                    {/*<div className="keyboard-button">*/}
                    {/*    <p className="button-text">Click me</p>*/}
                    {/*</div>*/}
                    <div className="keyboard-button" id="add-button" onClick={this.props.addButtonClickHandler}>
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                            <path d="M24 10h-10v-10h-4v10h-10v4h10v10h4v-10h10z"/>
                        </svg>
                    </div>
                    {/*<div className="keyboard-button">*/}
                    {/*    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">*/}
                    {/*        <path d="M24 10h-10v-10h-4v10h-10v4h10v10h4v-10h10z"/>*/}
                    {/*    </svg>*/}
                    {/*</div>*/}
                    {/*<div className="keyboard-button">*/}
                    {/*    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">*/}
                    {/*        <path d="M24 10h-10v-10h-4v10h-10v4h10v10h4v-10h10z"/>*/}
                    {/*    </svg>*/}
                    {/*</div>*/}
                    {/*<div className="keyboard-button"></div>*/}
                    {/*<div className="keyboard-button"></div>*/}
                    {/*<div className="keyboard-button"></div>*/}
                    {/*<div className="keyboard-button"></div>*/}
                </div>
            </div>
        )
    }
}

export default KeyboardWidget
