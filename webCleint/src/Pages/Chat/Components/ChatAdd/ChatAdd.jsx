import React, { useEffect } from 'react'
import "./ChatAdd.css"
import chatAddIcon from "../../../../assets/Icons/addIcon.svg"


function AddButtonHandler()
{
    const chatContactAddScreen = document.querySelector(".chat-contact-add-screen")
    // chatContactAddScreen.style.display = "flex"
    chatContactAddScreen.classList.add("active")
    
}




function ChatAdd() {


 useEffect(()=>{

     document.querySelector(".chat-add-btn").addEventListener("click",(e)=>{
         e.preventDefault() ;
         AddButtonHandler() ;
     })
},[])




  return (
    <div className="chat-add-btn">
        <img src={chatAddIcon} loading='lazy' alt="chat-icon" />
    </div>
  )
}

export default ChatAdd