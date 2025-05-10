import React, { useEffect, useState } from "react";
import { Input, Button, Select } from "antd";
import { motion } from "framer-motion";
import { toast } from "react-toastify";
import { apiConnector } from "services/apiConnector";
import { PRODUCTS, BRANDS, CATEGORIES } from "services/apis";

interface Product {
  name: string;
  description: string;
  price: number;
  quantity: number;
  category: string;
  brand: string;
}

const CreateProduct: React.FC = () => {
  const [product, setProduct] = useState<Product>({
    name: "",
    description: "",
    price: 0,
    quantity: 0,
    category: "",
    brand: "",
  });
  const [brands, setBrands] = useState<{ id: string; name: string }[]>([]);
  const [categories, setCategories] = useState<{ id: string; name: string }[]>(
    [],
  );
  const [loading, setLoading] = useState(false);

  const handleChange = (field: string, value: string | number) => {
    setProduct((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  useEffect(() => {
    // Fetching all categories and brands
    (async () => {
      try {
        const brandsRes = await apiConnector({
          method: "GET",
          url: BRANDS,
        });
        const categoriesRes = await apiConnector({
          method: "GET",
          url: CATEGORIES,
        });
        setBrands(brandsRes.data.brands);
        setCategories(categoriesRes.data.categories);
      } catch (err) {
        toast.error(
          "Something went wrong while fetching brands and categories!",
        );
      }
    })();
  }, []);

  const handleSubmit = async () => {
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
    const id = toast.loading("Please wait...");

    try {
      console.log(product);
      await apiConnector({ method: "POST", url: PRODUCTS, bodyData: product });
      toast.update(id, {
        render: "Saved!",
        type: "success",
        isLoading: false,
        autoClose: 2000,
      });
      setLoading(false);
    } catch (err) {
      console.log(err);
      toast.update(id, {
        render: "Something went wrong! Please try again later!",
        type: "error",
        isLoading: false,
        autoClose: 5000,
      });
      setLoading(false);
    }
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
          onChange={(e) => handleChange("price", Number(e.target.value))}
        />
        <Input
          placeholder="Quantity"
          type="number"
          value={product.quantity}
          onChange={(e) => handleChange("quantity", Number(e.target.value))}
        />
        <p>
          Category:{" "}
          <Select
            className="w-full"
            value={product?.category || undefined}
            onChange={(value) =>
              setProduct((prev) => (prev ? { ...prev, category: value } : prev))
            }
            options={categories.map((cat) => ({
              label: cat.name,
              value: cat.id,
            }))}
          />
        </p>

        <p>
          Brand:{" "}
          <Select
            className="w-full"
            value={product?.brand || undefined}
            onChange={(value) =>
              setProduct((prev) => (prev ? { ...prev, brand: value } : prev))
            }
            options={brands.map((brand) => ({
              label: brand.name,
              value: brand.id,
            }))}
          />
        </p>
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
