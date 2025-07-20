import React, { useEffect } from 'react'
import "./ChatContactAdd.css"
import leftArrowIcon from "../../assets/Icons/leftArrowIcon.svg"
import { addChatContact } from '../../Hooks/ChatHook';
import { useNavigate } from 'react-router-dom';
import { memo } from 'react';


function closeChatContactAddScreenHandler(event)
{
   event.preventDefault() ;
   const chatContactAddScreen = document.querySelector(".chat-contact-add-screen")
   chatContactAddScreen.classList.remove("active") ;

}


async function mobileAddButtonHandler()
{
    const loader = document.querySelector(".loader-green-hr")
    loader.classList.add("active")
    const MobileNumber = document.querySelector("#mobile-number-add-input").value 
    console.log(MobileNumber)
    const data = await addChatContact({MobileNumber : MobileNumber}) ;
    if(data["success"])
    {
       location.reload();
    }

    else 
    {
        document.querySelector(".add-error-msg").style.display = "block" ;
    }
    loader.classList.remove("active")

}





function ChatContactAdd({userId}) {


  

    
useEffect(()=>{
    
     const closeScreenButton = document.querySelector(".left-arrow-icon") ;
     closeScreenButton.addEventListener("click",closeChatContactAddScreenHandler) ;

     const mobileAddButton = document.querySelector(".mobile-add-button") ;
     mobileAddButton.addEventListener("click", (e) => {
      e.preventDefault()
      mobileAddButtonHandler()})

},[])

  return (
    <div className="chat-contact-add-screen">
          <div className="screen-header">
             <img loading='lazy' src={leftArrowIcon} alt="left-arrow-icon" className='left-arrow-icon' />
             <h2>Add Contact Here...</h2>
          </div>
          <input type="text" maxLength={10} placeholder='9876543213' id='mobile-number-add-input'/>
          <button className='mobile-add-button'>Add Contact</button>
          <p className='add-error-msg'>User not found</p>
    </div>
  )
}

export default memo(ChatContactAdd)