import React from 'react'
import "./Loader.css"
import ChatIcon from "../../assets/Icons/chat-dots-svgrepo-com.svg"

function Loader() {
  return (
    <div className="loader">
        <div className="logo">
          <img src={ChatIcon} alt="chat-icon" />
          <h1>Locito Chat</h1>
        </div>
        <div className="animated-loading"></div>
    </div>
  )
}

export default Loader