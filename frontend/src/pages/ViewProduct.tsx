import React, { useEffect, useState } from "react";
import { Layout, Skeleton } from "antd";
import Breadcrumbs from "components/Breadcrumbs";
import { useParams, useSearchParams } from "react-router-dom";
import { motion } from "framer-motion";
import { apiConnector } from "services/apiConnector";
import { PRODUCTS, CATEGORIES, BRANDS } from "services/apis";
import { toast } from "react-toastify";
import ProductDetails from "components/ProductDetails";
import ProductEditor from "components/ProductEditor";
import ProductImage from "components/ProductImage";

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

interface updateProduct {
  id: string;
  name: string;
  description: string;
  price: number;
  quantity: number;
  category: string | null;
  brand: string | null;
}

const ViewProduct: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [imageLoaded, setImageLoaded] = useState(false);
  const [product, setProduct] = useState<Product | null>(null);
  const [updatedProduct, setUpdatedProduct] = useState<updateProduct | null>(
    null,
  );
  const [brands, setBrands] = useState<{ id: string; name: string }[]>([]);
  const [categories, setCategories] = useState<{ id: string; name: string }[]>(
    [],
  );
  const [searchParams] = useSearchParams();
  const isEdit = searchParams.get("edit") === "true";
  const handleImageLoad = () => {
    setImageLoaded(true);
  };

  useEffect(() => {
    if (!id) return;

    // Fetching Product details
    (async () => {
      try {
        const res = await apiConnector({
          method: "GET",
          url: PRODUCTS + id + "/",
        });
        if (!res || !res.data || !res.data.product) {
          throw new Error("Something went wrong");
        }
        setProduct(res.data.product);
        setUpdatedProduct({
          id: res.data.product.id,
          name: res.data.product.name,
          description: res.data.product.description,
          quantity: res.data.product.quantity,
          price: res.data.product.price,
          brand: null,
          category: null,
        });
      } catch (err) {
        console.log(err);
        toast.error("Something went wrong! Please try again later!");
      }
    })();

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
  }, [id]);

  const updateProduct = async () => {
    if (!updatedProduct) return;

    if (!updatedProduct.brand) {
      toast.error("Please choose a brand");
      return;
    }

    if (!updatedProduct.category) {
      toast.error("Please choose a category");
      return;
    }

    const toastId = toast.loading("Please Wait...");
    try {
      await apiConnector({
        method: "PUT",
        url: PRODUCTS + id + "/",
        bodyData: updatedProduct,
      });

      toast.update(toastId, {
        render: "Product Updated Successfully",
        type: "success",
        autoClose: 5000,
        isLoading: false,
      });
    } catch (err) {
      console.log(err);
      toast.update(toastId, {
        render: "Something went wrong! Could not update!",
        type: "error",
        autoClose: 5000,
        isLoading: false,
      });
    }
  };

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
                {isEdit && (
                  <>
                    <ProductImage
                      handleImageLoad={handleImageLoad}
                      id={id}
                      imageLoaded={imageLoaded}
                    />
                    {product ? (
                      <ProductEditor
                        updateProduct={updateProduct}
                        brands={brands}
                        categories={categories}
                        setUpdatedProduct={setUpdatedProduct}
                        updatedProduct={updatedProduct}
                      />
                    ) : (
                      <Skeleton active />
                    )}
                  </>
                )}
                {!isEdit && (
                  <>
                    <ProductImage
                      handleImageLoad={handleImageLoad}
                      id={id}
                      imageLoaded={imageLoaded}
                    />
                    {product ? (
                      <ProductDetails product={product} />
                    ) : (
                      <Skeleton active />
                    )}
                  </>
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
