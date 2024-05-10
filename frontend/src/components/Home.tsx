import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Details from "./Details";
import Header from "./Header";
import { LiaEdit } from "react-icons/lia";
interface ChatBox {
  id: number;
  chatname: string;
  chatdesc: string;
}

export const Home: React.FC = () => {
  const [box, setBox] = useState<ChatBox[]>([]);
  const [state, setState] = useState(false);
  const [data, setData] = useState<any | null>(null);
  const navigate = useNavigate();

  const getInfo = async () => {
    try {
      const response = await fetch("http://localhost:8000/allInfo");
      if (!response.ok) {
        throw new Error("Failed to fetch data");
      }
      const data = await response.json();
      const dataArray = Array.isArray(data) ? data : [data];
      setBox(dataArray);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  useEffect(() => {
    getInfo();
  }, []);

  const fetchData = async (index: number) => {
    try {
      const response = await fetch(
        `http://localhost:8000/getInfo/${index + 1}`
      );
      if (!response.ok) {
        throw new Error("Failed to fetch data");
      }
      const data = await response.json();
      setState(true);
      setData(data);
      return data;
    } catch (error) {
      console.error("Error:", error);
    }
  };

  if (state) {
    return <Details data={data} />;
  }
  return (
    <div>
      <Header />
      <div className="flex justify-between mt-6 mx-5">
        <h1 className="text-[20px] font-bold">My Stack</h1>
        <button className="bg-green-500 p-2 font-bold rounded-xl">
          + New Stack
        </button>
      </div>
      <div className="border border-gray-300 mt-3"></div>
      <div className="flex flex-wrap ml-12 mt-10">
        {box.map((item, index) => (
          <div key={index} className="border border-gray-300 w-[300px] m-2 p-5">
            <h1 className="text-lg font-bold">{item.chatname}</h1>
            <h2 className="text-sm text-gray-500">{item.chatdesc}</h2>
            <button
              onClick={() => fetchData(index)}
              className="mt-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 border border-gray-300 rounded text-[10px] flex gap-2 pl-2"
            >
              Edit Stack
              <LiaEdit />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Home;
