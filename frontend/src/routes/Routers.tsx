import { Routes, Route, Navigate } from "react-router-dom";
import { Home } from "../components/Home";
import Details from "../components/Details";

const Router = () => {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/home" />} />
      <Route path="/home" element={<Home />} />
      <Route path="/details/:id" element={<Details data={undefined} />} />
    </Routes>
  );
};

export default Router;
