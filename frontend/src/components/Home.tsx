import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Details from "./Details";
import Header from "./Header";
import { LiaEdit } from "react-icons/lia";
import { GrClose } from "react-icons/gr";

interface ChatBox {
  id: number;
  chatname: string;
  chatdesc: string;
}

export const Home: React.FC = () => {
  const [boxes, setBoxes] = useState<ChatBox[]>([]);
  const [selectedBox, setSelectedBox] = useState<ChatBox | null>(null);
  const [chatname, setChatname] = useState("");
  const [isPopupOpen, setIsPopupOpen] = useState(false);
  const [chatdesc, setChatdesc] = useState("");
  const [state, setState] = useState(false);
  const [data, setData] = useState<any | null>(null);
  const navigate = useNavigate();

  const getAllInfo = async () => {
    try {
      const response = await fetch("http://localhost:8000/allInfo");
      if (!response.ok) {
        throw new Error("Failed to fetch data");
      }
      const data = await response.json();
      const dataArray = Array.isArray(data) ? data : [data];
      setBoxes(dataArray);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  useEffect(() => {
    getAllInfo();
  }, []);

  const fetchBoxDetails = async (id: number) => {
    try {
      const response = await fetch(`http://localhost:8000/getInfo/${id}`);
      if (!response.ok) {
        throw new Error("Failed to fetch data");
      }
      const data = await response.json();
      setState(true);
      setData(data);
      setSelectedBox(data);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleBoxClick = (id: number) => {
    fetchBoxDetails(id);
    navigate(`/details/${id}`); // Navigate to details page with the ID
  };

  const createStack = () => {
    setIsPopupOpen(true);
  };

  const closepopup = () => {
    setIsPopupOpen(false);
  };

  const handleSubmit = async () => {
    try {
      const response = await fetch("http://localhost:8000/createChatBox", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          chatName: chatname,
          chatDesc: chatdesc,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to create chat box");
        setIsPopupOpen(false);
      }

      setChatname("");
      setChatdesc("");
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
      <div className="">
        <div className="flex justify-between mt-6 mx-5">
          <h1 className="text-[20px] font-bold">My Stack</h1>
          <button
            className="bg-green-500 p-2 font-bold rounded-xl"
            onClick={createStack}
          >
            + New Stack
          </button>
        </div>
        <div className="border border-gray-300 mt-3"></div>
        <div className="flex flex-wrap ml-12 mt-10">
          {boxes.map((box) => (
            <div
              key={box.id}
              className="border border-gray-300 w-[300px] m-2 p-5"
            >
              <h1 className="text-lg font-bold">{box.chatname}</h1>
              <h2 className="text-sm text-gray-500">{box.chatdesc}</h2>

              <button
                onClick={() => handleBoxClick(box.id)}
                className="mt-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 border border-gray-300 rounded text-[10px] flex gap-2 pl-2"
              >
                Edit Stack
                <LiaEdit />
              </button>
            </div>
          ))}
        </div>
      </div>
      {isPopupOpen && (
        <div className="fixed top-0 left-0 w-full h-full bg-gray-700 bg-opacity-50 flex justify-center items-center">
          <div className="bg-white rounded-lg p-6 h-3/4 w-3/4 flex flex-col">
            <form className="flex flex-col items-center mt-6 mx-5">
              <GrClose className="" onClick={closepopup} />
              <h1 className="text-lg font-bold mb-2">Chat Name</h1>
              <input
                type="text"
                placeholder="Enter chat name"
                value={chatname}
                onChange={(e) => setChatname(e.target.value)}
                className="border border-gray-300 px-3 py-2 rounded-md mb-4 w-full max-w-md"
              />
              <h1 className="text-lg font-bold mb-2">Chat Description</h1>
              <textarea
                placeholder="Enter chat description"
                value={chatdesc}
                onChange={(e) => setChatdesc(e.target.value)}
                className="border border-gray-300 px-3 py-2 rounded-md mb-4 w-full max-w-md resize-none"
                rows={4}
              ></textarea>
              <button
                type="button"
                className="bg-green-500 text-white py-2 px-4 font-bold rounded-md hover:bg-green-600 transition-colors duration-300"
                onClick={handleSubmit}
              >
                Submit
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Home;
