import React, { Component } from 'react';
import {Product} from './Product.js';

class ProductList extends Component {

  render() {
	  return (
		<div>
		  {this.props.products.map(product => <Product key={product.rid} {...product} />)}
		</div>
	  );
  }
};

export default ProductList

