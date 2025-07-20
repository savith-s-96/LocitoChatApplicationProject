import React, { memo, useEffect, useRef } from 'react'
import "./ActiveChat.css"
import leftArrowIcon from "../../assets/Icons/leftArrowIcon.svg"
import userIcon from "../../assets/Icons/userDefaultIcon.svg"
import { useDispatch, useSelector } from 'react-redux'
import { Host } from '../../Hooks/Configuartion'
import sendIcon from "../../assets/Icons/sendIcon.svg"
import { useChatMessages } from '../../Hooks/ChatHook'
import RealTimeChatHanlder from '../../Hooks/Websocket'
function ActiveChat() {


   const chatUserProfile = useSelector( state => state.activeChat )
   const chatUserMessages = useSelector( state => state.chatUserMessages[chatUserProfile["chatRoomId"]]) 
   const chatReceiverId = chatUserProfile["chatUserId"]
   const inputMessageElement = useRef()
   const messagesElement = useRef()
   const chatSenderId = useSelector( state => state.userProfile["id"])
   const chatRoomId = chatUserProfile["chatRoomId"]
   const dispatch = useDispatch()
   let lastMessageId = -1;
   // console.log(chatUserMessages)




   function sendMessageHandler(e)
   {
    e.preventDefault()
    const message = inputMessageElement.current.value ;
    if(message)
    {
      RealTimeChatHanlder.send({senderId : chatSenderId, recieverId : chatReceiverId, message : message, chatRoomId : chatRoomId, dispatch : dispatch, messageId : lastMessageId + 1})
      inputMessageElement.current.value = ""
    }
  
   }


 
   useEffect(()=>{

    if(chatUserMessages)
    {

    
     
      const scrollPostion = chatUserMessages["scrollPosition"]
      // console.log(chatUserMessages)
      if(scrollPostion)
      {
        // console.log("scroll position",scrollPostion);
        messagesElement.scrollTop = scrollPostion 
      }

      else 
      {
         messagesElement.current.scrollTop = messagesElement.current.scrollHeight ;
      }

       const loader = document.querySelector(".messages span:last-child") 
      //  console.log(loader)
       const observer = new IntersectionObserver((entries)=>
      {

        //  console.log(entries[0].target)
         if(entries[0].isIntersecting && chatUserMessages["hasMore"])
         {
            // console.log(chatUserMessages["messages"].length)
            let lastMessageTimeStamp ;
            if(chatUserMessages["messages"].length > 0 )
            {

               lastMessageTimeStamp = chatUserMessages["messages"][chatUserMessages["messages"].length - 1]["messageTimeStamp"]
               lastMessageId = chatUserMessages["messages"][chatUserMessages["messages"].length - 1]["id"]
            }

            else 
            {
               lastMessageTimeStamp = Date.now() / 1000 ;
            }



            useChatMessages({chatRoomId : chatRoomId, receiverId : chatReceiverId ,lastMessageTimeStamp : lastMessageTimeStamp, dispatch : dispatch, messagesElement : messagesElement})
            observer.unobserve(entries[0].target)
         }

         else 
         {

           if(!chatUserMessages["hasMore"])
           {
            observer.unobserve(entries[0].target)
           }
 
         //  console.log(entries[0].target)
          entries[0].target.classList.remove("loader")
         }
      })

      observer.observe(loader)
    }


   },[chatUserMessages])

    
        
       function closeActiveWindow(e)
       {

        e.preventDefault() ;
        const activeWindow = document.querySelector(".active-chat-window")
        activeWindow.classList.remove("active")
       }

  return (
    
    <div className="active-chat-window">
      
       <div className="chat-profile-info">
          <div className="left-arrow" onClick={closeActiveWindow}>
            <img src={leftArrowIcon} alt="" />
          </div>
          <div className="profile-image-name">
            <div className="profile-name">
                <h2>{chatUserProfile["userName"] ? chatUserProfile["userName"] : chatUserProfile["mobileNumber"]}</h2>
            </div>
            <div className="profile-image">
                <img loading='lazy' src={chatUserProfile["profileImageUrl"] ? `${Host}/user/profile?filePath=${chatUserProfile["profileImageUrl"]}` : userIcon} />
            </div>
          </div>
       </div>

       <div className="messages" ref={messagesElement}>
           
           {
            
            chatUserMessages && chatUserMessages["messages"].map((chat,index)=>
            {
              
              return (
                  <div key={index} className={`message ${chat["userType"]}`}>
                     <p>{chat["message"]}</p>
                  </div>
              )
            })
          
           }
           <span className=""></span>
       </div>
       <div className="sending-msg-input">
            <textarea name="sendText" id="message-send-input" ref={inputMessageElement}></textarea>
            <div className="send-icon" onClick={sendMessageHandler}>
              <img src={sendIcon} alt="send" />
            </div>
       </div>

    </div>

  )
}

export default ActiveChat