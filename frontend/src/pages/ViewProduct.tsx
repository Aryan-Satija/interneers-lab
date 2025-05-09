import React, { useEffect, useState } from "react";
import { Layout, Skeleton, Button, Input, Select } from "antd";
import Breadcrumbs from "components/Breadcrumbs";
import { useParams, useSearchParams } from "react-router-dom";
import { motion } from "framer-motion";
import { apiConnector } from "services/apiConnector";
import { PRODUCTS, CATEGORIES, BRANDS } from "services/apis";
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
                        <h2 className="text-2xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                          <Input
                            value={updatedProduct?.name}
                            onChange={(e) =>
                              setUpdatedProduct((prev) =>
                                prev ? { ...prev, name: e.target.value } : prev,
                              )
                            }
                          />
                        </h2>
                        <p className="text-gray-600 mb-4">
                          <Input.TextArea
                            rows={3}
                            value={updatedProduct?.description}
                            onChange={(e) =>
                              setUpdatedProduct((prev) =>
                                prev
                                  ? { ...prev, description: e.target.value }
                                  : prev,
                              )
                            }
                          />
                        </p>
                        <div className="text-sm text-gray-500 flex flex-col gap-2">
                          <p>
                            Price: ₹{" "}
                            <Input
                              type="number"
                              value={updatedProduct?.price}
                              onChange={(e) =>
                                setUpdatedProduct((prev) =>
                                  prev
                                    ? { ...prev, price: Number(e.target.value) }
                                    : prev,
                                )
                              }
                            />
                          </p>
                          <p>
                            Quantity:{" "}
                            <Input
                              type="number"
                              value={updatedProduct?.quantity}
                              onChange={(e) =>
                                setUpdatedProduct((prev) =>
                                  prev
                                    ? {
                                        ...prev,
                                        quantity: Number(e.target.value),
                                      }
                                    : prev,
                                )
                              }
                            />
                          </p>
                          <p>
                            Category:{" "}
                            <Select
                              className="w-full"
                              value={updatedProduct?.category || undefined}
                              onChange={(value) =>
                                setUpdatedProduct((prev) =>
                                  prev ? { ...prev, category: value } : prev,
                                )
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
                              value={updatedProduct?.brand || undefined}
                              onChange={(value) =>
                                setUpdatedProduct((prev) =>
                                  prev ? { ...prev, brand: value } : prev,
                                )
                              }
                              options={brands.map((brand) => ({
                                label: brand.name,
                                value: brand.id,
                              }))}
                            />
                          </p>
                        </div>
                        <div>
                          <Button
                            type="default"
                            className="mt-4"
                            onClick={updateProduct}
                          >
                            Update
                          </Button>
                        </div>
                      </>
                    ) : (
                      <Skeleton active />
                    )}
                  </>
                )}
                {!isEdit && (
                  <>
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
                        <p className="text-gray-600 mb-4">
                          {product.description}
                        </p>
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
