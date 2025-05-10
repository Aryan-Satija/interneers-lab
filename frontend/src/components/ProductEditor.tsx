import React from "react";
import { Button, Input, Select } from "antd";

interface updateProduct {
  id: string;
  name: string;
  description: string;
  price: number;
  quantity: number;
  category: string | null;
  brand: string | null;
}

interface productEditorProps {
  updateProduct: () => Promise<void>;
  updatedProduct: updateProduct | null;
  setUpdatedProduct: React.Dispatch<React.SetStateAction<updateProduct | null>>;
  categories: { id: string; name: string }[];
  brands: { id: string; name: string }[];
}

const ProductEditor: React.FC<productEditorProps> = ({
  updateProduct,
  updatedProduct,
  setUpdatedProduct,
  categories,
  brands,
}) => {
  return (
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
              prev ? { ...prev, description: e.target.value } : prev,
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
                prev ? { ...prev, price: Number(e.target.value) } : prev,
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
        <Button type="default" className="mt-4" onClick={updateProduct}>
          Update
        </Button>
      </div>
    </>
  );
};

export default ProductEditor;
