import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Bookmark, Eye, Pencil } from "lucide-react";
import { motion } from "framer-motion";
import { Skeleton } from "antd";

interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  quantity: number;
  category: string;
  brand: string;
}

interface productListInterface {
  data: Product[];
}

const Productlist: React.FC<productListInterface> = ({ data }) => {
  const navigate = useNavigate();

  const [bookmark, setBookmark] = useState<Product[]>([]);

  useEffect(() => {
    if (bookmark.length > 0)
      localStorage.setItem("bookmarked", JSON.stringify(bookmark));
  }, [bookmark]);

  useEffect(() => {
    if (localStorage.getItem("bookmarked") !== null) {
      setBookmark((prev) =>
        JSON.parse(localStorage.getItem("bookmarked") || "[]"),
      );
    }
  }, []);

  const toggleBookmark = (product: Product) => {
    setBookmark((prev) => {
      return prev.some((item) => item.id === product.id)
        ? prev.filter((item) => item.id !== product.id)
        : [...prev, product];
    });
  };

  const [imageLoaded, setImageLoaded] = useState<Record<number, boolean>>({});

  const handleImageLoad = (index: number) => {
    setImageLoaded((prev) => ({ ...prev, [index]: true }));
  };

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 p-6 w-[80%] mx-auto">
      {data.map((product, index) => {
        return (
          <motion.div
            key={index}
            initial={{ opacity: 0, scale: 0.8, y: 30 }}
            whileInView={{ opacity: 1, scale: 1, y: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ duration: 0.4, delay: index * 0.05 }}
            className="bg-white cursor-pointer rounded-xl shadow-md hover:shadow-lg transition-shadow duration-300 px-4 flex flex-col items-start relative overflow-hidden"
          >
            <div className="absolute top-[8px] left-4 flex gap-4 z-10">
              <Eye
                size={22}
                className="text-gray-600 hover:text-sky-600 cursor-pointer hover:animate-ping"
                onClick={() => {
                  navigate(`/products/${product.id}`);
                }}
              />
              <Bookmark
                size={22}
                className={`cursor-pointer hover:animate-ping ${
                  bookmark.some((item) => item.id === product.id)
                    ? "text-sky-600 -translate-y-1"
                    : "text-gray-600"
                }`}
                onClick={() => toggleBookmark(product)}
              />
              <Pencil
                size={22}
                className="text-gray-600 hover:text-sky-600 cursor-pointer hover:animate-ping"
                onClick={() => {
                  navigate(`/products/${product.id}?edit=true`);
                }}
              />
            </div>

            {!imageLoaded[index] && (
              <div className="w-full h-[20rem] mt-8 mb-2 flex flex-col items-center justify-center">
                <Skeleton.Image
                  style={{ width: "100%", height: "100%" }}
                  active
                />
              </div>
            )}
            <img
              src={`https://picsum.photos/200/300?random=${index}`}
              alt="avatar"
              className={`w-full rounded-md h-[20rem] mt-8 mb-2 ${!imageLoaded[index] ? "hidden" : ""}`}
              onLoad={() => {
                handleImageLoad(index);
              }}
            />

            <h3 className="text-lg font-semibold text-gray-800">
              {product.name}
            </h3>
            <p className="text-sm text-gray-500">{product.description}</p>
            <div className="my-4 w-full text-right text-sky-600 font-semibold">
              ₹{product.price}
            </div>
          </motion.div>
        );
      })}
    </div>
  );
};

export default Productlist;
