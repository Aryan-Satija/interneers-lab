import React from "react";
import { Routes, Route } from "react-router-dom";
import Home from "pages/Home";
import Product from "pages/Product";
import ViewProduct from "pages/ViewProduct";
import "./App.css";

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/products" element={<Product />} />
        <Route path="/products/:id" element={<ViewProduct />} />
      </Routes>
    </div>
  );
}

export default App;
