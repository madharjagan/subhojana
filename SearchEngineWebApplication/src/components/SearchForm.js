import React, { Component } from 'react';
import {
FormGroup,
FormControl,
Button,
Form
}
from 'react-bootstrap'

var axios = require('axios');

class SearchForm extends Component {

  state = { 
  value: ''
  };

  getValidationState() {
    /*const length = this.state.value.length;
    if (length > 10) return 'success';
    else if (length > 5) return 'warning';
    else if (length > 0) return 'error';
    return null;*/
  };

  handleChange(event) {
    this.setState({ value: event.target.value });
  };
  
  handleSubmit = (event) => {
	console.log("Called ...");
    event.preventDefault();
	var qstr = 'searchstring=' + escape(this.state.value);
    axios.get(`http://localhost:5000/subhojana?${qstr}`)
      .then(resp => {
	    console.log(resp.data);
        this.props.onShowSearchResults(resp.data);
      });
  };
  
 
  render() {
    return (
		<div className="row col-md-12">
	      <Form inline bsClass="col-md-12"onSubmit={this.handleSubmit.bind(this)}>
        <FormGroup
          controlId="formBasicText"
          validationState={this.getValidationState()}
        >
          <FormControl
            type="text"
			bsClass="input-lg col-md-8"
            value={this.state.value}
            placeholder="Recipe Name"
            onChange={this.handleChange.bind(this)}
          />
          <FormControl.Feedback />
        </FormGroup>
	   <Button bsClass="btn btn-info btn-lg" value="Search" type="submit">Recipizz</Button>
      </Form>
	 </div>
    );
  }
}

export default SearchForm;

