import React from "react";
import { Button } from "antd";

interface paginationControlProps {
  page: number;
  totalPages: number;
  setPage: React.Dispatch<React.SetStateAction<number>>;
}

const PaginationControl: React.FC<paginationControlProps> = ({
  page,
  totalPages,
  setPage,
}) => {
  return (
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
  );
};

export default PaginationControl;
