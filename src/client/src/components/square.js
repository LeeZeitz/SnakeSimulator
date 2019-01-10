import React from 'react';
import btoa from 'btoa';

const colors = ['white', 'yellow', 'blue', 'red'];


const Square = (props) => {
    var data = '';
    for (var i = 0; i < props.image.byteLength; ++i) {
        data += String.fromCharCode(props.image[i]);
    }
    return (
        <div className='square' style={ {backgroundColor: colors[props.value]} } src={ "data:image/jpeg;base64," + btoa(data) } >
            { props.value }
        </div>
    )    
    /*
    else {
        return (
            <div className='square' style={ {backgroundColor: colors[props.value]} } >
                { props.value }
            </div>
        )
    }
    */
};

export default Square;