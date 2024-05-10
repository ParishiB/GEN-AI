import { FiSave } from "react-icons/fi";
import { CgProfile } from "react-icons/cg";

const Header = () => {
  return (
    <>
      <div className="grid grid-cols-2 m-2">
        <div className="flex items-center mb-2">
          <img src="src/assets/logo.png" alt="" className="h-[30px]" />
          <h1 className="font-bold ml-2">GENAI Stack</h1>
        </div>
        <div className="flex justify-end items-center">
          <button className="flex items-center mr-2 shadow p-3 border border-black rounded-xl">
            <FiSave className="font-semibold" />
            <div className="ml-2 font-semibold">Save</div>
          </button>
          <CgProfile className="h-[50px] ml-2" />
        </div>
      </div>
    </>
  );
};

export default Header;
