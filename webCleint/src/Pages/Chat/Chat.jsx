import React, { useEffect } from 'react'
import "./Chat.css"
import Navigation from './Components/Navigation/Navigation'
import Search from './Components/Search/Search'
import ChatList from './Components/ChatList/ChatList'
import { useLocation } from 'react-router-dom'
import ChatAdd from './Components/ChatAdd/ChatAdd'
// import ChatContactAdd from '../../Component/ChatContactAdd/ChatContactAdd'
import { Suspense, lazy } from 'react'
import Profile from '../../Component/Profile/Profile'
import ActiveChat from '../ActiveChat/ActiveChat'
import RealTimeChatHanlder from '../../Hooks/Websocket'
import { useDispatch } from 'react-redux'
import notificationSound from "../../assets/sounds/notification.mp3"
const ChatContactAdd = lazy(()=>{ return import("../../Component/ChatContactAdd/ChatContactAdd")})


function Chat() {

  const location = useLocation()
  const {userId} = location.state
  const dispatch = useDispatch()
  
  useEffect(()=>{

     if(userId != undefined)
     {
        // console.log(userId)
       RealTimeChatHanlder.connect({senderId: userId})
       RealTimeChatHanlder.dispatch = dispatch;
     }
    
  },[])


  return (
  
    <div className="chat-page">
 
      <div className="notification-sound">
             <audio src={notificationSound} controls></audio>
      </div>
     <Navigation/>
     <ChatList userId={userId}/>
     <ChatAdd/>
     <Suspense fallback={<div>Loading...</div>}>
     <ChatContactAdd userId={userId}/>
     </Suspense>
     <Profile/>
     <ActiveChat/>
    </div>

  )
}

export default Chat