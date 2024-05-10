import create from "zustand";

interface AgentState {
  agentname: string; // Corrected spelling here
  role: string;
  goal: string;
  backstory: string;
  capability: string;
  task: string;
  setAgentName: (agentname: string) => void; // Corrected spelling here
  setRole: (role: string) => void;
  setGoal: (goal: string) => void;
  setBackstory: (backstory: string) => void;
  setCapability: (capability: string) => void;
  setTask: (task: string) => void;
}

export const useAgentStore = create<AgentState>((set) => ({
  agentname: "", // Corrected spelling here
  role: "",
  goal: "",
  backstory: "",
  capability: "",
  task: "",
  setAgentName: (agentname) => set({ agentname }), // Corrected spelling here
  setRole: (role) => set({ role }),
  setGoal: (goal) => set({ goal }),
  setBackstory: (backstory) => set({ backstory }),
  setCapability: (capability) => set({ capability }),
  setTask: (task) => set({ task }),
}));

const Agent = () => {
  const {
    agentname, // Corrected spelling here
    role,
    goal,
    backstory,
    capability,
    task,
    setAgentName, // Corrected spelling here
    setRole,
    setGoal,
    setBackstory,
    setCapability,
    setTask,
  } = useAgentStore();

  return (
    <div className="border border-gray-300 p-4 w-[350px] rounded-xl">
      <form>
        <h1 className="font-bold">Agents</h1>
        <div className="grid gap-2 text-gray-600">
          <h2 className="text-left">Agent Name</h2>
          <input
            value={agentname}
            onChange={(e) => setAgentName(e.target.value)}
            placeholder="writer"
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
          <h2 className="text-left">Role</h2>
          <input
            value={role}
            onChange={(e) => setRole(e.target.value)}
            placeholder="summarising expert"
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
          <h2 className="text-left">Goal</h2>
          <input
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            placeholder="summarize input into presentable points"
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
          <h2 className="text-left">Backstory</h2>
          <input
            value={backstory}
            onChange={(e) => setBackstory(e.target.value)}
            placeholder="Expert in summarising the given text"
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
          <h2 className="text-left">Capability</h2>
          <input
            value={capability}
            onChange={(e) => setCapability(e.target.value)}
            placeholder="llm_task_executor"
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
          <h2 className="text-left">Task</h2>
          <input
            value={task}
            onChange={(e) => setTask(e.target.value)}
            placeholder="summarise points"
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
        </div>
      </form>
    </div>
  );
};

export default Agent;
