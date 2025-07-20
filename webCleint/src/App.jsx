
import { unstable_HistoryRouter as HistoryRouter, Route, Routes } from "react-router-dom"
import "./App.css"
import Home from "./Pages/Home/Home.jsx"
import Login from "./Pages/Login/Login.jsx"
import Chat from "./Pages/Chat/Chat.jsx"
import customHistory from "./Hooks/customHistory.js"


function App() {
  return ( 
    <>
    <div className="loader-green-hr">
      <span  className="loader-loading"></span>
    </div>
    <HistoryRouter history={customHistory}>
      <Routes>
          
         <Route path="/" element={<Home/>} />
         <Route path="/login" element = {<Login/>} />
         <Route path="/chat" element={<Chat/>} />
      </Routes>
    </HistoryRouter>
    </>
  )
}

export default App