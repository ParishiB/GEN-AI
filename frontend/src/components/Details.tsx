import React, { useEffect, useState } from "react";
import { TbFolderOpen } from "react-icons/tb";
import { IoMenuOutline } from "react-icons/io5";
import { IoSparklesOutline } from "react-icons/io5";
import { GoTools } from "react-icons/go";
import { TbMessageCircle2Filled } from "react-icons/tb";
import { GrClose } from "react-icons/gr";
import "reactjs-popup/dist/index.css";
import { FaPlay } from "react-icons/fa";
import Header from "./Header";
import Agent from "./Agent";
import LLM from "./LLM";
import { useLLMStore } from "./LLM";
import { useAgentStore } from "./Agent";
interface DetailsProps {
  data: any;
}

const Details: React.FC<DetailsProps> = ({ data }) => {
  const [isHovered, setIsHovered] = useState(false);
  const [isPopupOpen, setIsPopupOpen] = useState(false);
  const [showAgent, setShowAgent] = useState(false);
  const [showLLM, setShowLLM] = useState(false);
  const [showLLM2, setShowLLM2] = useState(false);
  const [showLLM3, setShowLLM3] = useState(false);
  const [res, setRes] = useState(false);
  const [res1, setRes1] = useState("");
  const [messageInput, setMessageInput] = useState("");
  const [isButtonDisabled, setIsButtonDisabled] = useState(false);

  const { openaiapibase, openaiapikeys, llm } = useLLMStore();

  const { agentname, role, goal, backstory, capability, task } =
    useAgentStore();

  useEffect(() => {
    fetchButtonDisabledStatus(data.id);
  }, []);

  const openAgentForm = () => {
    setShowAgent(!showAgent);
  };

  const openAIForm = () => {
    setShowLLM(!showLLM);
  };

  const openAI2Form = () => {
    setShowLLM2(!showLLM2);
  };

  const openAI3Form = () => {
    setShowLLM3(!showLLM3);
  };

  const build_run = () => {
    if (!isButtonDisabled) {
      setIsPopupOpen(true);
    }
  };

  const fetchButtonDisabledStatus = async (chatBoxId: any) => {
    try {
      const response = await fetch(
        `http://localhost:8000/isButtonDisabled/${chatBoxId}`
      );
      if (response.ok) {
        const data = await response.json();
        setIsButtonDisabled(data.disabled);
      } else {
        console.error(
          "Failed to fetch button disabled status:",
          response.statusText
        );
      }
    } catch (error) {
      console.error("Error fetching button disabled status:", error);
    }
  };

  const sendMessage = async () => {
    try {
      const response = await fetch("http://localhost:8000/generateResponse", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          chatgpt_request: {
            prompt: messageInput,
          },
          agent_info: {
            agentname: "Agent Smith",
            role: "Support Agent",
            goal: "Help the customer",
            backstory: "Experienced in customer service",
            capability: "Problem-solving skills",
            task: "Resolve customer issues",
          },
        }),
      });

      const responseData = await response.json();
      setRes(true);
      setRes1(responseData.response);
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  const build_stack = async () => {
    const chatBoxId = data.id;
    try {
      await fetch(
        `http://localhost:8000/insert_role_goal_temperature/${chatBoxId}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            role: role,
            goal: goal,
            temperature: 0.7, // Hardcoded temperature value
            backstory: backstory,
            maxtokens: 100, // Hardcoded maxtokens value
          }),
        }
      );

      await fetch(`http://localhost:8000/insert_task/${chatBoxId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          task: task,
          backstory: backstory,
          capability: capability,
        }),
      });

      await fetch(`http://localhost:8000/insert_openai_keys/${chatBoxId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          openaiapibase: openaiapibase,
          openaiapikeys: openaiapikeys,
          llm: llm,
          agentname: agentname,
        }),
      });

      console.log("API calls completed successfully");
    } catch (error) {
      console.error("An error occurred while making API calls:", error);
    }
  };

  return (
    <>
      <Header />
      <div className="grid grid-cols-[30%_auto] ml-5">
        <div className="">
          <button className="flex items-center p-3 m-2 border border-gray-400 rounded-xl mr-2 w-[200px]">
            <div className="font-medium">{data.chatname}</div>
            <TbFolderOpen className="ml-1" />
          </button>
          <h1 className="font-semibold ml-5">Agents</h1>
          <button
            className="flex items-center justify-between p-3 m-2 border border-gray-400 rounded-xl mr-2 w-[200px]"
            onClick={openAgentForm}
          >
            <h3 className="mr-3">Agents</h3>
            <IoMenuOutline />
          </button>

          <div className="flex p-2">
            <GoTools />
            <h1 className="font-semibold ml-1">Tools</h1>
          </div>
          <button className="flex items-center justify-between p-3 m-2 border border-gray-400 rounded-xl mr-2 w-[200px]">
            <h3 className="mr-3">Wikisearch</h3>
            <IoMenuOutline />
          </button>
          <button className="flex items-center justify-between p-3 m-2 border border-gray-400 rounded-xl mr-2 w-[200px]">
            <h3 className="mr-3">DuckDuck search</h3>
            <IoMenuOutline />
          </button>
          <button className="flex items-center justify-between p-3 m-2 border border-gray-400 rounded-xl mr-2 w-[200px]">
            <h3 className="mr-3">GMail</h3>
            <IoMenuOutline />
          </button>
          <button className="flex items-center justify-between p-3 m-2 border border-gray-400 rounded-xl mr-2 w-[200px]">
            <h3 className="mr-3">Github</h3>
            <IoMenuOutline />
          </button>
          <div className="flex p-3">
            <IoSparklesOutline />
            <h1 className="font-semibold ml-1">LLMs</h1>
          </div>
          <button
            className="flex items-center justify-between p-3 m-2 border border-gray-400 rounded-xl mr-2 w-[200px]"
            onClick={openAIForm}
          >
            <h3 className="mr-3">OpenAI 3.5</h3>
            <IoMenuOutline />
          </button>
          <button
            className="flex items-center justify-between p-3 m-2 border border-gray-400 rounded-xl mr-2 w-[200px]"
            onClick={openAI2Form}
          >
            <h3 className="mr-3">OpenAI 4</h3>
            <IoMenuOutline />
          </button>
          <button
            className="flex items-center justify-between p-3 m-2 border border-gray-400 rounded-xl mr-2 w-[200px]"
            onClick={openAI3Form}
          >
            <h3 className="mr-3">Azure OpenAI</h3>
            <IoMenuOutline />
          </button>
        </div>
        <div className="">
          <div className="flex gap-6">
            {showAgent && <Agent />}

            {(showLLM && <LLM name={"openAI 3.5"} />) ||
              (showLLM2 && <LLM name={"openAI 4"} />) ||
              showLLM3 || <LLM name={"Azure OpenAI"} />}
          </div>

          <div className="absolute bottom-5 right-5 flex justify-end items-end space-x-2 mb-4 mr-4">
            <button
              className="bg-green-600 rounded-xl w-[40px] h-[40px] flex justify-center items-center"
              onClick={build_stack}
            >
              <FaPlay className="text-white" />
              {isHovered && (
                <span className="absolute top-[-30px] left-[-10px] bg-black text-white px-2 py-1 rounded">
                  Build Stack
                </span>
              )}
            </button>
            <button
              className={`bg-blue-600 rounded-xl w-[40px] h-[40px] flex justify-center items-center ${
                isButtonDisabled ? "opacity-50 cursor-not-allowed" : ""
              }`}
              onClick={build_run}
            >
              <TbMessageCircle2Filled className="text-white" />
            </button>
            {isPopupOpen && (
              <div className="fixed top-0 left-0 w-full h-full bg-gray-700 bg-opacity-50 flex justify-center items-center">
                <div className="bg-white rounded-lg p-6 h-3/4 w-3/4 flex flex-col">
                  <button
                    onClick={() => setIsPopupOpen(false)}
                    className=" top-0 right-0 mt-2 ml-6"
                  >
                    <GrClose />
                  </button>
                  <div className="flex-grow">
                    {res ? (
                      <div>{res1}</div>
                    ) : (
                      <div className="text-center mt-24">
                        <div className="">
                          <h1 className="font-bold">GenAI Stack Chat</h1>
                        </div>

                        <h2>
                          Start a conversation to inspect the chaining process
                        </h2>
                      </div>
                    )}
                  </div>
                  <div className="flex gap-5">
                    <input
                      type="text"
                      placeholder="Send a message"
                      onChange={(e) => setMessageInput(e.target.value)}
                      className="w-11/12 border border-gray-300 rounded-md p-2"
                    />
                    <button
                      className="bg-green-600 rounded-xl w-[40px] h-[40px] flex justify-center items-center"
                      onClick={sendMessage}
                    >
                      <FaPlay className="text-white" />
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
};

export default Details;
