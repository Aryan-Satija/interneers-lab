import React from "react";
import Breadcrumbs from "./Breadcrumbs";
function Navbar() {
  return (
    <div className="w-full p-4 fixed top-0 left-0 flex flex-row">
      <Breadcrumbs />
    </div>
  );
}

export default Navbar;
