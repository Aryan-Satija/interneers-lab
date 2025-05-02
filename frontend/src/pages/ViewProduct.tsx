import React, { useEffect, useState } from "react";
import { Layout, Skeleton } from "antd";
import Breadcrumbs from "components/Breadcrumbs";
import { useParams } from "react-router-dom";
import { motion } from "framer-motion";

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
  color: "#111",
  backgroundColor: "#f0f0f1",
  overflow: "auto",
  padding: "2rem",
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

const ViewProduct: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [imageLoaded, setImageLoaded] = useState(false);
  const [product, setProduct] = useState<Product | null>(null);

  const handleImageLoad = () => {
    setImageLoaded(true);
  };

  useEffect(() => {
    //todo: make api call
    if (!id) return;
    setTimeout(() => {
      setProduct({
        id: id,
        name: "Laptop Pro",
        price: 1299,
        quantity: 20,
        description:
          "A professional-grade laptop featuring top-tier specifications, ideal for software developers, designers, and content creators.",
        category: "Laptops",
        brand: "Dell",
      });
    }, 1000);
  }, [id]);

  return (
    <div className="w-screen h-screen">
      <Layout style={layoutStyle}>
        <Sider width="15%" style={siderStyle}>
          <div className="m-4 rounded-full shadow-md shadow-gray-400 cursor-pointer overflow-hidden">
            <img
              src="https://api.dicebear.com/9.x/identicon/svg?seed=aryan"
              alt="avatar"
              className="w-full h-full object-cover transition-transform duration-300 ease-in-out hover:rotate-180"
            />
          </div>
        </Sider>

        <Layout className="rounded-md">
          <Header style={headerStyle}>
            <Breadcrumbs />
          </Header>

          <Content style={contentStyle}>
            {
              <motion.div
                initial={{ opacity: 0, y: 80 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 1 }}
                className="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-md text-left"
              >
                <div className="flex flex-col h-[440px] items-center justify-center w-full">
                  {!imageLoaded && (
                    <Skeleton.Image
                      style={{ width: "100%", marginBottom: 16 }}
                      active
                    />
                  )}
                  <img
                    src={`https://picsum.photos/600/400?random=${id}`}
                    alt="Product"
                    className={`rounded-lg w-full mb-4 ${!imageLoaded ? "hidden" : ""}`}
                    onLoad={handleImageLoad}
                  />
                </div>
                {product ? (
                  <>
                    <h2 className="text-2xl font-bold text-gray-800 mb-2">
                      {product.name}
                    </h2>
                    <p className="text-gray-600 mb-4">{product.description}</p>
                    <div className="text-sm text-gray-500">
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
                ) : (
                  <Skeleton active />
                )}
              </motion.div>
            }
          </Content>
        </Layout>
      </Layout>
    </div>
  );
};

export default ViewProduct;
