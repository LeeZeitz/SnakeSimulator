import openSocket from 'socket.io-client';

const socket = openSocket('127.0.0.1:5000')


const startGame = (cb) => {
    socket.on('board', board => {
        console.log(board);
        socket.emit('message', {'message': 'got it!'});
        cb(board);
    })
    socket.emit('startGame', {'message': 'Start Game!'});
}


export default startGame