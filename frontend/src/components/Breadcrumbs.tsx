import React from "react";
import { Link, useLocation } from "react-router-dom";

const Breadcrumbs: React.FC = () => {
  const location = useLocation();
  const path = location.pathname.split("/").filter((x) => x !== "");

  return (
    <nav className="text-lg text-gray-600 my-2">
      <ol className="list-reset flex">
        <li>
          <Link to="/" className="text-blue-600 hover:underline">
            Home
          </Link>
        </li>
        {path.map((name, index) => {
          const routeTo = "/" + path.slice(0, index + 1).join("/");

          return (
            <li key={routeTo} className="flex items-center">
              <span className="mx-2">/</span>
              {index === path.length - 1 ? (
                <span>{name}</span>
              ) : (
                <Link to={routeTo} className="text-blue-600 hover:underline">
                  {name}
                </Link>
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
};

export default Breadcrumbs;
