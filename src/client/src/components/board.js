import React, { Component } from 'react';
import Square from './square';

// Props:
//      board: board object
//
class Board extends Component {

    renderSquare(i) {
        return <Square key={ i } />;
    }

    renderSquares = () => {
        let board = [];
        let count = 0;
        for (let i = 0; i < this.props.board.height; i++) {
            let squares = []
            for (let j = 0; j < this.props.board.width; j++) {
                squares.push(
                    this.renderSquare(count)
                );
                count++;
            }
            board.push(
                <div key={ count } className='board-row'>
                    { squares }
                </div>
            );
        }
        return board;
    }

    /*
    renderSnakeHeads = () => {
        this.props.board.snakes.forEach(snake => {
            
        });
    }
    */

    render() {
        return (
            <div className='board'>
                { this.renderSquares() }
            </div>
        )
    }
    
}

export default Board;