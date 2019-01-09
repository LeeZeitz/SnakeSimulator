import React from 'react';


const colors = ['white', 'yellow', 'blue', 'red'];


const Square = (props) => {
    return (
        <div className='square' style={ {backgroundColor: colors[props.value]} } >
            { props.value }
        </div>
    )
};

export default Square;