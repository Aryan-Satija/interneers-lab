import React from "react";
import { Skeleton } from "antd";

interface productImageProps {
  id: string | undefined;
  handleImageLoad: () => void;
  imageLoaded: boolean;
}
const ProductImage: React.FC<productImageProps> = ({
  id,
  handleImageLoad,
  imageLoaded,
}) => (
  <div className="flex flex-col h-[440px] items-center justify-center w-full">
    {!imageLoaded && (
      <Skeleton.Image style={{ width: "100%", marginBottom: 16 }} active />
    )}
    <img
      src={`https://picsum.photos/600/400?random=${id}`}
      alt="Product"
      className={`rounded-lg w-full mb-4 ${!imageLoaded ? "hidden" : ""}`}
      onLoad={handleImageLoad}
    />
  </div>
);

export default ProductImage;
