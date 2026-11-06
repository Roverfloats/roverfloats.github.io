
import { useEffect, useState } from "react";
import Header from "../components/Header";
import NavBar from "../components/NavBar";
import { useNavigate } from "react-router-dom";

function Home({ setUser }) {
    const [userList, setUserList] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [creatingNewUser, setCreatingNewUser] = useState(false);
    const [input, setInput] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        async function fetchUsers() {
            try {
                const response = await fetch("http://127.0.0.1:5000/api/users");

                if (!response.ok) {
                    throw new Error(`HTTP error: ${response.status}`);
                }

                const json = await response.json();

                setUserList(
                    typeof json === "string" ? JSON.parse(json) : json
                );

            } catch (error) {
                console.error("Error fetching users:", error);
                setError(error.message);
            } finally {
                setLoading(false);
            }
        }

        fetchUsers();
    }, []);

    // Customisable loading layout
    if (loading) {
        return (
            <div className="loading-container">
                <h2>Loading...</h2>
                <p>Please wait while we fetch your users.</p>
                {/* Add your own spinner or animation here */}
            </div>
        );
    }

    if (error) {
        return (
            <div className="error-container">
                <h2>Something went wrong</h2>
                <p>{error}</p>
            </div>
        );
    }

  function choseUser(user) {
    setUser(user);
    navigate("/practice");
  }

function updateInput(e) {
      setInput(e.target.value);
  }

  function cancel() {
    setUser("");
    setCreatingNewUser(false)
  }


async function createNewUser() {
    try {
        const response = await fetch(
            "http://127.0.0.1:5000/api/new-user",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    user: input
                }),
            }
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Failed to create user");
        }

        setCreatingNewUser(false)

            try {
        const response = await fetch("http://127.0.0.1:5000/api/users");

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        const json = await response.json();

        setUserList(
            typeof json === "string" ? JSON.parse(json) : json
        );

    } catch (error) {
        console.error("Error fetching users:", error);
        setError(error.message);
    } finally {
        setLoading(false);
    }

    } catch (error) {
        console.error("Error creating user:", error);
    }
}


    return (
        <>
            <Header />
            <NavBar />

            {!creatingNewUser ? 
                <div className="w-full flex justify-center">
                    <div className="border-black border-2 rounded-[20px] w-[80%] p-10 flex items-center flex-row justify-center">
                        {userList.users.map((user) => (
                                <button onClick={() => choseUser(user)} className="p-5 flex border-black border-2 rounded-[20px] m-5 min-w-[100px] min-h-[100px] max-w-[100px] max-h-[100px] cursor-pointer hover:bg-black transition duration-100 ease-in-out justify-center items-center cursor-pointer">
                                    <p className="text-white text-wrap">{user}</p>
                                </button>
                            ))
                        }
                            <button onClick={() => setCreatingNewUser(true)} className="p-5 flex border-black border-2 rounded-[20px] m-5 min-w-[100px] min-h-[100px] max-w-[100px] max-h-[100px] cursor-pointer hover:bg-black transition duration-100 ease-in-out justify-center items-center cursor-pointer">
                                <p className="text-white text-wrap">Create New User</p>
                            </button>
                    </div>
                </div>
                :
                <div className="w-full flex justify-center">
                    <div className="border-black border-2 rounded-[20px] w-[80%] p-10 flex items-center flex-row justify-center">
                        <div className="w-[400px]">
                            <input className={`border-black border-2 rounded-[20px] w-full h-10 bg-[#494949] flex text-center text-white mb-10`} type="text" placeholder="ユーザー" onChange={updateInput} value={input}/>
                            <div className="flex mt-5 w-[400px] flex-row justify-between">
                                <button onClick={() => cancel()} className="border-black border-2 rounded-[20px] w-[150px] h-8 text-white cursor-pointer hover:bg-black transition duration-100 ease-in-out">Cancel</button>
                                <button onClick={() => createNewUser()} className="border-black border-2 rounded-[20px] w-[150px] h-8 text-white cursor-pointer hover:bg-black transition duration-100 ease-in-out">Create New User</button>
                            </div>
                        </div>
                    </div>
                </div>
            }

        </>
    );
}

export default Home;
