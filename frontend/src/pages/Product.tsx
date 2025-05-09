import React, { useEffect, useState } from "react";
import { Button, Layout } from "antd";
import Breadcrumbs from "components/Breadcrumbs";
import Sidebar from "components/Sidebar";
// import data from "../data.json";
import Productlist from "components/Productlist";
import CreateProduct from "components/createProduct";
import { useLocalStorage } from "@uidotdev/usehooks";
import { apiConnector } from "services/apiConnector";
import { PRODUCTS } from "services/apis";
import { toast } from "react-toastify";

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
  const [bookmark, setBookmark] = useLocalStorage<Product[]>(
    "bookmark/product",
    [],
  );
  const [data, setData] = useState<Product[]>([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  useEffect(() => {
    (async () => {
      try {
        const res = await apiConnector({
          method: "GET",
          url: PRODUCTS + `?page=${page}`,
        });
        if (!res || !res.data || !res.data.products) {
          throw new Error("Something went wrong");
        }
        setData(res.data.products);
        setTotalPages(Math.floor((res.data.total_products + 9) / 10));
      } catch (err) {
        console.log(err);
        toast.error("Unable to load products. Please try again later.");
      }
    })();
  }, [page]);
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
              <>
                <div className="w-full flex flex-row items-center justify-center gap-[2rem]">
                  <Button
                    type="default"
                    onClick={() => {
                      setPage(page - 1);
                    }}
                    disabled={page === 1}
                  >
                    PREV
                  </Button>
                  <p>
                    showing {page} of {totalPages} pages
                  </p>
                  <Button
                    type="default"
                    disabled={page === totalPages}
                    onClick={() => {
                      setPage(page + 1);
                    }}
                  >
                    NEXT
                  </Button>
                </div>
                <Productlist
                  data={data}
                  bookmark={bookmark}
                  setBookmark={setBookmark}
                />
              </>
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
