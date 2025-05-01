import React from "react";
import { LayoutGrid, PencilRuler, Bookmark } from "lucide-react";

interface SidebarProps {
  mode: number;
  setMode: React.Dispatch<React.SetStateAction<number>>;
}

const Sidebar: React.FC<SidebarProps> = ({ mode, setMode }) => {
  return (
    <div>
      <div className="m-4 rounded-full shadow-md shadow-gray-400 cursor-pointer overflow-hidden">
        <img
          src="https://api.dicebear.com/9.x/identicon/svg?seed=aryan"
          alt="avatar"
          className="w-full h-full object-cover transition-transform duration-300 ease-in-out hover:rotate-180"
        />
      </div>
      <div className="my-16">
        <div
          className={
            mode === 0
              ? "text-xl ml-4 rounded-l-lg my-4 bg-[#f0f0f1] flex items-center justify-start px-8 gap-4 py-2 cursor-pointer text-sky-600 font-semibold"
              : "text-xl ml-4 rounded-l-lg my-4 cursor-pointer text-gray-400 flex items-center justify-start px-8 gap-4 py-2 font-semibold"
          }
          onClick={() => {
            setMode(0);
          }}
        >
          <div>
            <LayoutGrid />
          </div>
          <div>Products</div>
        </div>
        <div
          className={
            mode === 1
              ? "text-xl ml-4 rounded-l-lg my-4 bg-[#f0f0f1] flex items-center justify-start px-8 gap-4 py-2 cursor-pointer text-sky-600 font-semibold"
              : "text-xl ml-4 rounded-l-lg my-4 cursor-pointer text-gray-400 flex items-center justify-start px-8 gap-4 py-2 font-semibold"
          }
          onClick={() => {
            setMode(1);
          }}
        >
          <div>
            <PencilRuler />
          </div>
          <div>Create</div>
        </div>
        <div
          className={
            mode === 2
              ? "text-xl ml-4 rounded-l-lg my-4 bg-[#f0f0f1] flex items-center justify-start px-8 gap-4 py-2 cursor-pointer text-sky-600 font-semibold"
              : "text-xl ml-4 rounded-l-lg my-4 cursor-pointer text-gray-400 flex items-center justify-start px-8 gap-4 py-2 font-semibold"
          }
          onClick={() => {
            setMode(2);
          }}
        >
          <div>
            <Bookmark />
          </div>
          <div>Bookmarked</div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
