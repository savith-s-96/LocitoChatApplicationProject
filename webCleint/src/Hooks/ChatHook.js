import { Host} from "./Configuartion";
import { get_access_token } from "./AuthenticationHook";
import { useDispatch } from "react-redux";
import { addChatMessage, changeUserChatMessageState } from "../ReduxStore/slices/ChatMessagesSlice";

export async function getChatList({pageOffset})
{
  const url = `${Host}/chat/get-chat-rooms?pageOffset=${pageOffset}`
  const response = await fetch(url, {credentials : "include"})
  let data = await response.json()
  
  if(data["access_token"] == 'false')
  {
     data = await get_access_token() ;

     if(data)
     {
        return await getChatList({pageOffset})
     }

     else 
     {
      return false
     }

  }

  else 
  {
   
   
  if(response.status == 200)
  {
    return data["chatContacts"]
  }

  else 
  {
    return false
  }

  }

}


export async function addChatContact({MobileNumber})
{
  const url = `${Host}/chat/add-contact` 
  const response = await fetch(url, {
      method : "POST",
      body : JSON.stringify({"MobileNumber" : MobileNumber}),
      headers : {
        "Content-Type" : "application/json",
      },
       credentials : "include",
      
  })

  let data = await response.json()

  if(data["access_token"] == 'false')
  {
     data = await get_access_token() ;

     if(data)
     {
        return await addChatContact({MobileNumber : MobileNumber})
     }

     else 
     {
      return false
     }

  }

  else 
  {
    
      return data

  }


  
}


export async function useChatMessages({chatRoomId, receiverId, lastMessageTimeStamp, dispatch, messagesElement}) 
{
 

  // console.log("fetch request send")

  const url = `${Host}/chat/getmessages?chatRoomId=${chatRoomId}&lastMessageTimeStamp=${lastMessageTimeStamp}`
  const response = await fetch(url, {credentials : "include"})
  let data = await response.json()
  
  if(data["access_token"] == 'false')
  {
     data = await get_access_token() ;

     if(data)
     {
         await useChatMessages({chatRoomId:chatRoomId, receiverId : receiverId, lastMessageTimeStamp : lastMessageTimeStamp})
     }

     else 
     {
      return false
     }

  }

  else 
  {
   
   
  if(response.status == 200)
  {
    const formatted_data = []

    if(data["messages"].length > 0)
    {
      for (let message of data["messages"])
      {
       formatted_data.push({"id" : message["id"], "message" : message["text"], "senderId" : message["sender_id"], "receiverId" : message["receiver_id"],"messageTimeStamp" : message["message_time"],"userType" : receiverId == message["receiver_id"] ? "sender" : "receiver" })
      }

    dispatch(addChatMessage({chatUserId : chatRoomId, messages : formatted_data }))
    }

    else 
    {
     document.querySelector(".messages span").classList.remove("loader")
     dispatch(changeUserChatMessageState({"chatRoomId" : chatRoomId,"stateName" : "hasMore", "stateValue" : false}))
    }
    
    // console.log(messagesElement.current.scrollTop)
    dispatch(changeUserChatMessageState({"chatRoomId" : chatRoomId,"stateName" : "scrollPosition", "stateValue" : messagesElement.current.scrollTop}))
    
    

    
  }

  else 
  {
    return false
  }

  }

}


  
