import React, { Component } from 'react';
import Square from './square';

// Props:
//      board: Board object
//
class Board extends Component {

    renderSquare(i, value, head_image) {
        return <Square key={ i } value={ value } image={ head_image } />;
    }

    renderSquares = () => {

        let foods = [];
        let bodies = [];
        let heads =[];
        let snakes = [];
        
        if (Object.keys(this.props.board).length > 0) {

            foods = this.props.board.food;
            snakes = this.props.board.snakes;
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
                let head_image = '';

                if (JSON.stringify(foods).indexOf(JSON.stringify([j, i])) !== -1){
                    value = 1;
                }

                for (let k = 0; k < snakes.length; k++){
                    if (JSON.stringify(snakes[k].body).indexOf(JSON.stringify([j, i])) !== -1) {
                        value = 3;
                        break;
                    }

                    else if (JSON.stringify(snakes[k].head).indexOf(JSON.stringify([j, i])) !== -1) {
                        value = 2;
                        head_image = snakes[k].head_image;
                        break;
                    }
                };

                squares.push(
                    this.renderSquare(count, value, head_image)
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