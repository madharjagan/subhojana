import React, { Component } from 'react';
import ingredentsImage from'../images/ingredents.svg';
import makeImage from'../images/makerecipes.png';

import {
	  Form
}
from 'react-bootstrap'


var axios = require('axios');

const divStyle = {display:'none'};


class Product extends Component {
		
	getIngredience = (event) => {
		console.log("Called getIngredience...");
		event.preventDefault();
		var qstr = 'page_url=' + escape(this.props.receipe_page_url);
		var ingredience = document.getElementById("ingredience"+this.props.rid);
		if (ingredience.style.display === "none") {
			axios.get(`http://localhost:5000/getIngredient?${qstr}`)
			  .then(resp => {
				ingredience.innerHTML = resp.data;
				ingredience.style.display = "block";
			});
		} 
		else {
				ingredience.style.display = "none";
 		}
	};
	
	getMakeRecipes = (event) => {
		console.log("Called getIngredience...");
		event.preventDefault();
		var qstr = 'page_url=' + escape(this.props.receipe_page_url);
		var ingredience = document.getElementById("ingredience"+this.props.rid);
		if (ingredience.style.display === "none") {
			axios.get(`http://localhost:5000/getIngredient?${qstr}`)
			  .then(resp => {
				ingredience.innerHTML = resp.data;
				ingredience.style.display = "block";
			});
		} 
		else {
				ingredience.style.display = "none";
 		}
	};
	
  render() {
  return (
		<div className="col-md-9">
			<div className="row">
				<div className="col">
					<a href={""+this.props.receipe_page_url}><h2>{this.props.receipe_title}</h2></a>
				</div>
			</div>
			<div className="row">
				<br />
			</div>
			<div className="row">
			  <div className="col-md-3 col-xs-4 col-sm-2">
				  <img width="150" height="200" src={""+ this.props.receipe_page_image} alt={""+this.props.receipe_page_image} /> 
			  </div>
			  
			  <div className="col-md-8 col-xs-8 col-sm-10">
				<p align="justify"><br/>{this.props.receipe_page_description}</p>
				<Form>
					<a href="#" onClick={this.getIngredience.bind(this)}><img src={ingredentsImage} alt="ingredents"/></a>
					<a href="#" onClick={this.getMakeRecipes.bind(this)}><img src={makeImage} alt="Make Recipes" width="40.392px" height="40.392px"/></a>
				</Form>
			  </div>
			</div>
			<div className="row">
				<br />
			</div>
			<div className="row">
				<div id={"ingredience" + this.props.rid} style={divStyle}>
				</div>
			</div>
		</div>
	  );
  }
};

export {Product}