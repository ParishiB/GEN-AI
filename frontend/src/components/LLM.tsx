import { useEffect } from "react";
import create from "zustand";

interface LLMProps {
  name: string;
}

interface LLMState {
  maxtokens: number;
  openaiapibase: string;
  openaiapikeys: string;
  temperature: number;
  llm: string;
  setmaxtokens: (value: number) => void;
  setopenaiapibase: (value: string) => void;
  setopenaiapikeys: (value: string) => void;
  setTemperature: (value: number) => void;
  setLlm: (value: string) => void;
}

export const useLLMStore = create<LLMState>((set) => ({
  maxtokens: 100,
  openaiapibase: "",
  openaiapikeys: "",
  temperature: 0.7, // Set temperature to 0.7 by default
  llm: "",
  setmaxtokens: (value) => set({ maxtokens: value }),
  setopenaiapibase: (value) => set({ openaiapibase: value }),
  setopenaiapikeys: (value) => set({ openaiapikeys: value }),
  setTemperature: (value) => set({ temperature: value }),
  setLlm: (value) => set({ llm: value }),
}));

const LLM: React.FC<LLMProps> = ({ name }: LLMProps) => {
  const {
    maxtokens,
    openaiapibase,
    openaiapikeys,
    temperature,
    llm,
    setmaxtokens,
    setopenaiapibase,
    setopenaiapikeys,
    setTemperature,
    setLlm,
  } = useLLMStore();

  useEffect(() => {
    setLlm(name);
  }, [name, setLlm]);

  return (
    <div className="border border-gray-300 p-4 w-[350px] rounded-xl">
      <form>
        <h1 className="font-bold">{name}</h1>

        <div className="grid gap-2 text-gray-600">
          <h2 className="text-left">Max Tokens</h2>
          <input
            value={maxtokens}
            onChange={(e) => setmaxtokens(parseInt(e.target.value))}
            placeholder="100"
            type="number"
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
          <h2 className="text-left">AI Engine</h2>
          <input
            value={openaiapibase}
            onChange={(e) => setopenaiapibase(e.target.value)}
            placeholder="AI Engine"
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
          <h2 className="text-left">OpenAI API Keys</h2>
          <input
            value={openaiapikeys}
            onChange={(e) => setopenaiapikeys(e.target.value)}
            placeholder="OpenAI API keys"
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
          <h2 className="text-left">Temperature</h2>
          <input
            value={temperature} // Set value to 0.7
            placeholder="0.7"
            disabled // Disable input so the user can't modify it
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
        </div>
      </form>
    </div>
  );
};

export default LLM;
