import { Link } from "react-router-dom"

function NavBar() {
  return (
    <>
        <div className="flex justify-center items-center mb-10">
            <div className="flex divide-x-2 divide-black divide-solid border-black border-2 rounded-b-[20px] overflow-hidden">
                <Link className="text-white px-8 py-2 hover:bg-black transition duration-100 ease-in-out" to="/">Main</Link>
                <Link className="text-white px-8 py-2 hover:bg-black transition duration-100 ease-in-out" to="/statistics">Stats</Link>
                <Link className="text-white px-8 py-2 hover:bg-black transition duration-100 ease-in-out" to="/configuration">Config</Link>
            </div>
        </div>
    </>
  )
}

export default NavBar
