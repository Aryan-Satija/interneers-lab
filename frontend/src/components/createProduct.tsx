import React, { useState } from "react";
import { Input, Button } from "antd";
import { motion } from "framer-motion";
import { toast } from "react-toastify";

const CreateProduct: React.FC = () => {
  const [product, setProduct] = useState({
    name: "",
    description: "",
    price: "",
    quantity: "",
    category: "",
    brand: "",
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (field: string, value: string) => {
    setProduct((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleSubmit = () => {
    if (
      !product.name ||
      !product.description ||
      !product.price ||
      !product.quantity ||
      !product.category ||
      !product.brand
    ) {
      toast.error("All fields are mandatory!");
      return;
    }

    setLoading(true);
    const id = toast.loading("Saving...");

    //todo: call create product api

    setTimeout(() => {
      toast.update(id, {
        render: "Saved!",
        type: "success",
        isLoading: false,
        autoClose: 2000,
      });
      setLoading(false);
      console.log("Product created:", product);

      setProduct({
        name: "",
        description: "",
        price: "",
        quantity: "",
        category: "",
        brand: "",
      });
    }, 2000);
  };

  return (
    <motion.div
      className="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-md text-left"
      initial={{ opacity: 0, y: 80 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 1 }}
    >
      <h2 className="text-2xl font-semibold mb-4">Create Product</h2>
      <div className="space-y-4">
        <Input
          placeholder="Name"
          value={product.name}
          onChange={(e) => handleChange("name", e.target.value)}
        />
        <Input.TextArea
          placeholder="Description"
          rows={14}
          value={product.description}
          onChange={(e) => handleChange("description", e.target.value)}
        />
        <Input
          placeholder="Price"
          type="number"
          value={product.price}
          onChange={(e) => handleChange("price", e.target.value)}
        />
        <Input
          placeholder="Quantity"
          type="number"
          value={product.quantity}
          onChange={(e) => handleChange("quantity", e.target.value)}
        />
        <Input
          placeholder="Category"
          value={product.category}
          onChange={(e) => handleChange("category", e.target.value)}
        />
        <Input
          placeholder="Brand"
          value={product.brand}
          onChange={(e) => handleChange("brand", e.target.value)}
        />
        <Button
          type="default"
          onClick={handleSubmit}
          loading={loading}
          className="mt-2"
        >
          Create
        </Button>
      </div>
    </motion.div>
  );
};

export default CreateProduct;
