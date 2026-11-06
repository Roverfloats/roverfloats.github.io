import { useEffect, useState } from "react";

function Conjugation({user}) {
  const [data, setData] = useState(null);
  const [answerData, setAnswerData] = useState(null);
  const [answerGiven, setAnswerGiven] = useState(true);
  const [input, setInput] = useState("");

async function fetchWord() {
  const response = await fetch(
    "http://127.0.0.1:5000/api/data",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user: user
      }),
    }
  );

if (!response.ok) {
    const error = await response.text();
    console.error("Backend error:", error);
    throw new Error(error);
}

  let json = await response.json();

  if (typeof json === "string") {
    json = JSON.parse(json);
  }

  setData(json);
  return json;
}

  
  async function fetchAnswer(word) {
    const response = await fetch(
      "http://127.0.0.1:5000/api/answer",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          word: word,
          user: user,
        }),
      }
    );

if (!response.ok) {
    const error = await response.text();
    console.error("Backend error:", error);
    throw new Error(error);
}

    const json = await response.json();

    // Only needed if your Python function returns a JSON string
    const result =
      typeof json === "string" ? JSON.parse(json) : json;

    setAnswerData(result);
    return result;
  }


  async function GetNewWord() {
    setAnswerGiven(false)
    setInput("");
    setAnswerData(null)
    await fetchWord();
  }

  async function Answer() {
    setAnswerGiven(true)
    await fetchAnswer(input);
  }

  async function SkipWord() {
    setAnswerGiven(true)
    await fetchAnswer("");
  }

  function updateInput(e) {
      setInput(e.target.value);
  }

useEffect(() => {
  const handleKeyDown = (e) => {
    if (e.key !== "Enter") return;

    e.preventDefault();

    if (answerGiven) {
      GetNewWord();
    } else {
      Answer();
    }
  };

  window.addEventListener("keydown", handleKeyDown);

  return () => {
    window.removeEventListener("keydown", handleKeyDown);
  };
}, [answerGiven, input]);

  return (
    <div className="border-black border-2 rounded-[20px] w-full p-10 flex items-center flex-col">
        {data == null ? 
          <p className="text-[40px] text-white mt-2">日本語を勉強しましょう！</p>
        : ""}

        <p className="text-[20px] text-white">{data?.level}</p>
        <div className="flex w-50 h-5 rounded-full bg-black overflow-hidden">
          <div className="h-full bg-[#ff0000] rounded-full transition-all duration-1000" style={{ width: `${data?.progress ?? 0}%` }}/>
        </div>
        <p className="text-[30px] text-white">{data?.options}</p>
        <p className="text-[40px] text-white mt-2">{data?.hiragana}</p>
        <p className="text-[15px] text-white">{data?.english}</p>
        <p className="text-[15px] text-white">{data?.current_streak}</p>

        {answerData ?
        <>
          <p className="text-[30px] text-white mt-4">{answerData?.result}</p>
          <p className="text-[15px] text-white">{answerData?.misconjugation}</p>
          <p className="text-[15px] text-white">{answerData?.irregularity}</p>
          <p className="text-[15px] text-white">{answerData?.response_time}</p>
          

          {answerData?.result != "correct" ?
            <>
              <p className="text-[15px] text-white mt-4">The correct version would be:</p>
              <p className="text-[20px] text-white">{answerData?.correct_form}</p>
              <p className="text-[20px] text-white">The steps are:</p>
              <p className="text-[20px] text-white">{answerData?.step0}</p>
              <p className="text-[20px] text-white">{answerData?.step1}</p>
              <p className="text-[20px] text-white">{answerData?.step2}</p>
              <p className="text-[20px] text-white">{answerData?.step3}</p>
              <p className="text-[20px] text-white">{answerData?.step4}</p>
              <p className="text-[20px] text-white">{answerData?.step5}</p>
            </>
            : ""
          }
        </>
          :
          ""
      }
        <div className="w-[400px]">
            <input className={`border-black border-2 rounded-[20px] w-full h-10 bg-[#494949] flex text-center text-white mt-10 ${!answerGiven ? "flex" : "hidden" }`} type="text" placeholder="解答" onChange={updateInput} value={input}/> 
        </div>
        
          <div className={`mt-5 w-[400px]  flex-row justify-center ${answerGiven ? "flex" : "hidden" }`}>
            <button onClick={() => GetNewWord()} className="border-black border-2 rounded-[20px] w-[150px] h-8 text-white cursor-pointer hover:bg-black transition duration-100 ease-in-out">Next Word</button>
        </div>
        <div className={`mt-5 w-[400px]  flex-row justify-between ${!answerGiven ? "flex" : "hidden" }`} >
            <button onClick={() => Answer()} className="border-black border-2 rounded-[20px] w-[150px] h-8 text-white cursor-pointer hover:bg-black transition duration-100 ease-in-out">Submit Answer</button>
            <button onClick={() => SkipWord()} className="border-black border-2 rounded-[20px] w-[150px] h-8 text-white cursor-pointer hover:bg-black transition duration-100 ease-in-out">Skip Word</button>
        </div>
    </div>
  )
}

export default Conjugation
