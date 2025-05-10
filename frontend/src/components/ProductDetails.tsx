import React from "react";

interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  quantity: number;
  category: string;
  brand: string;
}

const ProductDetails: React.FC<{ product: Product }> = ({ product }) => {
  return (
    <>
      <h2 className="text-2xl font-bold text-gray-800 mb-2">{product.name}</h2>
      <p className="text-gray-600 mb-4">{product.description}</p>
      <div className="text-sm text-gray-500 flex flex-col gap-2">
        <p>Price: ₹{product.price}</p>
        <p>Quantity: {product.quantity}</p>
        <p>
          Category:{" "}
          <span className="text-sky-800 bg-sky-400/40 px-2 rounded-full">
            {product.category}
          </span>
        </p>
        <p>
          Brand:{" "}
          <span className="text-green-800 bg-green-400/40 px-2 rounded-full">
            {product.brand}
          </span>
        </p>
      </div>
    </>
  );
};

export default ProductDetails;
