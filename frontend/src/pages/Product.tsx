import React, { useState } from "react";
import { Layout } from "antd";
import Breadcrumbs from "components/Breadcrumbs";
import Sidebar from "components/Sidebar";
import data from "../data.json";
import Productlist from "components/Productlist";
import CreateProduct from "components/createProduct";
import { useLocalStorage } from "@uidotdev/usehooks";

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

const Product: React.FC = () => {
  const [mode, setMode] = useState<number>(0);
  const [bookmark, setBookmark] = useLocalStorage<Product[]>("bookmarked", []);
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
            {mode === 0 && (
              <Productlist
                data={data}
                bookmark={bookmark}
                setBookmark={setBookmark}
              />
            )}
            {mode === 1 && <CreateProduct />}
            {mode === 2 && (
              <Productlist
                data={bookmark}
                bookmark={bookmark}
                setBookmark={setBookmark}
              />
            )}
          </Content>
        </Layout>
      </Layout>
    </div>
  );
};

export default Product;
