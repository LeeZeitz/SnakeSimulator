import React, { Component } from 'react';
import Square from './square';

// Props:
//      board: Board object
//
class Board extends Component {

    renderSquare(i, value) {
        return <Square key={ i } value={ value } />;
    }

    renderSquares = () => {

        let foods = [];
        let bodies = [];
        let heads =[];
        
        if (Object.keys(this.props.board).length > 0) {

            foods = this.props.board.food;
            let snakes = this.props.board.snakes;
            snakes.forEach(snake => {
                heads.push(snake.head);
                bodies = bodies.concat(snake.body);
            });
        }

        let board = [];
        let count = 0;
        for (let i = 0; i < this.props.board.height; i++) {
            let squares = []
            for (let j = 0; j < this.props.board.width; j++) {
                let value = 0;
                if (JSON.stringify(foods).indexOf(JSON.stringify([j, i])) !== -1){
                    value = 1;
                }
                else if (JSON.stringify(bodies).indexOf(JSON.stringify([j, i])) !== -1) {
                    value = 3;
                }
                else if (JSON.stringify(heads).indexOf(JSON.stringify([j, i])) !== -1) {
                    value = 2
                }
                squares.push(
                    this.renderSquare(count, value)
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