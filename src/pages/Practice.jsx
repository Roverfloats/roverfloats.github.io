import Conjugation from "../components/conjugation"
import Header from "../components/Header"
import NavBar from "../components/NavBar"

function Practice({user}) {
    return (
        <>
            <Header/>
            <NavBar/>

            <div className="w-full flex justify-center">
                <div className="w-[80%] flex">
                    <Conjugation user={user}/>
                </div>
            </div>

            
        </>
    )
}

export default Practice
