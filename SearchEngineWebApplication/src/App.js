import React, { Component } from 'react';
import SearchForm from './components/SearchForm.js';
import ProductList from './components/ProductList.js';

class App extends Component {

  state = {
    products: []
  };

showSearchResults = (searchResults) => {
    this.setState(prevState => ({
      products: searchResults
    }));
};


  render() {
    return (
		<div>
			<SearchForm  onShowSearchResults={this.showSearchResults}/>
			<ProductList products = {this.state.products} />
		</div>
    );
  }
}

export default App;