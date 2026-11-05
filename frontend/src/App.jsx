import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './main.css'
import Home from './pages/Home';
import Statistics from './pages/Statistics';
import Configuration from './pages/Configuration';
import { useState } from 'react';
import Practice from './pages/Practice';

function App() {
  const [user, setUser] = useState("Hank");
  
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home setUser={setUser}/>} />
        <Route path="/practice" element={<Practice user={user}/>} />
        <Route path="/statistics" element={<Statistics />} />
        <Route path="/configuration" element={<Configuration />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
