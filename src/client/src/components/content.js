import React, { Component } from 'react';
import startGame from '../api';
import Board from './board';

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
            <div className='content'>
                <Board board={ this.state.board } />
            </div>
        )
    }
}

export default Content;