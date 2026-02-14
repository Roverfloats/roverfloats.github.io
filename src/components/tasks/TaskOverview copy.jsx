import { useNavigate } from "react-router";
import { useEffect, useState } from "react";
import { collection, query } from "firebase/firestore";
import { db } from "../../firebase";
import { FetchData } from "../../endpoints/General";
import Task from "./Task";

function TaskOverview({setReload, reload, setPopup, setPopupContent}) {
    const navigate = useNavigate();

    const [TaskData, setTaskData] = useState([]);

    useEffect(() => {
        const fetch = async () => {
            let q = collection(db, "Tasks");
            q = query(q);
            var taskData = await FetchData(q);
            setTaskData(taskData)
        }
        fetch();
    }, [reload]);

    return (
        <div className="flex-1 h-auto px-[50px]">
            <p className="text-black dark:text-white text-[25px] mt-[20px]">General Tasks</p>
            <div className="w-full h-[50px]">
                <button
                    className="h-[30px] text-[#0096FF] dark:text-[#0065AD]"
                    onClick={() => navigate("/tasks")}
                >Manage Tasks +</button>
            </div>
            <div className="divide-solid divide-y-2 divide-[#D0D0D0] dark:divide-[black]">
                <div>
                    <p className="text-black dark:text-white">Open Tasks</p>
                    {
                        TaskData.filter(x => x.presetId == "").map((task) => (
                            <Task
                                key={task.id}
                                taskData={task}
                                setReload={setReload}
                                setPopup={setPopup}
                                setPopupContent={setPopupContent}
                            />
                        ))
                    }                    
                </div>             
            </div>
        </div>
    )
}

export default TaskOverview
