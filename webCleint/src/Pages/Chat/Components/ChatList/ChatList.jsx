import React, { useEffect, useState } from 'react'
import "./ChatList.css"
import { getChatList } from '../../../../Hooks/ChatHook'
import userDefaultIcon from "../../../../assets/Icons/userDefaultIcon.svg"
import { Host } from '../../../../Hooks/Configuartion'
import { changeActiveChatUser } from '../../../../ReduxStore/slices/activeChatSlice'
import { useDispatch } from 'react-redux'
import { addChatUserId } from '../../../../ReduxStore/slices/ChatMessagesSlice'


function ChatList({userId}) 
{

  const [chatList, setChatList] = useState([])
  const [pageNumber, setPageNumber] = useState(0)
  const [lastChatList, setLastChatList] = useState(null)
 
  const dispatch = useDispatch()

  
  function activeChatHandler({chatUser})
  {
     
     dispatch(changeActiveChatUser(chatUser));
     const loader = document.querySelector(".messages span")
     const messagesElement = document.querySelector(".messages")
     messagesElement.scrollTop = messagesElement.scrollHeight ;
     loader.classList.add("loader")
     const chatWindow = document.querySelector(".active-chat-window") 
     chatWindow.classList.add("active")
  }
  

  

  useEffect(()=>{
    

    (async ()=>{

       const data = await getChatList({pageOffset:pageNumber}) ;
       
       
     if(data)
     {
       setChatList(prev => [...prev,...data]) ;
     }

    })()

    


  },[pageNumber])


  useEffect(()=>{


     if(lastChatList)
     {
      
     const observer = new IntersectionObserver((entries)=>{
      
      if(entries[0].isIntersecting)
      {
        
          observer.unobserve(entries[0].target)
          setPageNumber(prev => prev + 1)
        
      }
      
    })
     observer.observe(lastChatList)
     }

  },[lastChatList])

  useEffect(()=>{

     const currentLastChatList = document.querySelector(".chat-contact-profile:last-child")
     if(lastChatList != currentLastChatList)
     {
        setLastChatList(currentLastChatList)
     }

     if( chatList.length > 0)
     {
       for(let chatUser of chatList)
        {
          
          dispatch(addChatUserId({chatUserId:chatUser["chatRoomId"]}))
        } 
     }

  },[chatList])







  return (
    <div className="chat-list">
       {
         chatList.map((chat,index)=>{
            return (
            <div className="chat-contact-profile" key={index} onClick={(e)=>{ e.preventDefault(); activeChatHandler({chatUser : chat}) }}>
            <div className="profile-image">
            <img loading='lazy' src={ chat["profileImageUrl"] ? Host +"/user/profile?filePath="+ chat["profileImageUrl"] : userDefaultIcon}/>
            </div>
            <div className="profile-name">
              <h2>{chat["userName"] ?  chat["userName"] : chat["mobileNumber"]}</h2>
            </div>
           </div>
            )
         })
       }
    </div>
  )
}

export default ChatList