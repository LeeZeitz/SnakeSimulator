import React, { Component } from 'react';
import startGame from '../api';

class Content extends Component{

    constructor(props) {
        super(props)
        this.state = {
            board: {}
        }
        startGame(this.handleNewBoard)
    };

    handleNewBoard = (board) => {
        this.setState(
            {board}
        )
    };

    render() {
        return (
            <div>
                asuh dude
            </div>
        )
    }
}

export default Content;