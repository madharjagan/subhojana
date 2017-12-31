import React, { Component } from 'react';

class Popup extends Component {
  render() {
	  console.log(this.props.text);
    return (
      <div className='popup'>
        <div className='popup_inner'>
          <div className='ingredient'>{this.props.text}</div>
        <button onClick={this.props.closePopup}>close me</button>
        </div>
      </div>
    );
  }
};

export {Popup}