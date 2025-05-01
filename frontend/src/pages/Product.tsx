import React, { useState, useEffect } from "react";
import { Layout } from "antd";
import Breadcrumbs from "components/Breadcrumbs";
import { Bookmark, Eye, Pencil } from "lucide-react";
import data from "../data.json";
import { motion } from "framer-motion";
import Sidebar from "components/Sidebar";

const { Header, Sider, Content } = Layout;

const headerStyle: React.CSSProperties = {
  textAlign: "center",
  color: "#fff",
  height: 64,
  display: "flex",
  alignItems: "center",
  backgroundColor: "#fff",
};

const contentStyle: React.CSSProperties = {
  textAlign: "center",
  minHeight: 120,
  color: "#fff",
  backgroundColor: "#f0f0f1",
  overflow: "scroll",
};

const siderStyle: React.CSSProperties = {
  textAlign: "center",
  color: "#111",
  backgroundColor: "#fff",
};

const layoutStyle = {
  borderRadius: 8,
  overflow: "hidden",
  width: "100%",
  maxWidth: "100%",
  height: "100%",
};

interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  quantity: number;
  category: string;
  brand: string;
}

const Product: React.FC = () => {
  const [mode, setMode] = useState<number>(0);
  const [bookmark, setBookmark] = useState<Product[]>([]);
  const toggleBookmark = (product: Product) => {
    setBookmark((prev) => {
      return prev.some((item) => item.id === product.id)
        ? prev.filter((item) => item.id !== product.id)
        : [...prev, product];
    });
    localStorage.setItem("bookmarked", JSON.stringify(bookmark));
  };

  useEffect(() => {
    if (localStorage.getItem("bookmarked") !== null) {
      setBookmark((prev) =>
        JSON.parse(localStorage.getItem("bookmarked") || "[]"),
      );
    }
  }, []);

  return (
    <div className="w-screen h-screen">
      <Layout style={layoutStyle}>
        <Sider width="15%" style={siderStyle}>
          <Sidebar mode={mode} setMode={setMode} />
        </Sider>
        <Layout className="rounded-md">
          <Header style={headerStyle}>
            <Breadcrumbs />
          </Header>
          <Content style={contentStyle}>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 p-6 w-[80%] mx-auto">
              {data.map((product, index) => (
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
                    />
                  </div>

                  <img
                    src={`https://picsum.photos/200/300?random=${index}`}
                    alt="avatar"
                    className="w-full rounded-md h-[20rem] mt-8 mb-2"
                  />
                  <h3 className="text-lg font-semibold text-gray-800">
                    {product.name}
                  </h3>
                  <p className="text-sm text-gray-500">{product.description}</p>
                  <div className="my-4 w-full text-right text-sky-600 font-semibold">
                    ₹{product.price}
                  </div>
                </motion.div>
              ))}
            </div>
          </Content>
        </Layout>
      </Layout>
    </div>
  );
};

export default Product;
