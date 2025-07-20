import { addChatMessage } from "../ReduxStore/slices/ChatMessagesSlice";

export default class RealTimeChatHanlder
{

     static webSocketObject;
     static webSocketUrl = "wss://locitochatapplication.onrender.com/chat/ws/chat/send"
     static dispatch ;
     static NotificatioAudio ;
   

     static connect({senderId})
     {
         // console.log(senderId)
         RealTimeChatHanlder.webSocketObject = new WebSocket( `${RealTimeChatHanlder.webSocketUrl}?userId=${senderId}` )
         
         RealTimeChatHanlder.webSocketObject.onopen = ()=>{
            // console.log("connection open")
            RealTimeChatHanlder.NotificatioAudio = document.querySelector(".notification-sound audio")
      
         }

         RealTimeChatHanlder.webSocketObject.onmessage = (data)=>{
            data = JSON.parse(data["data"])
            RealTimeChatHanlder.dispatch( addChatMessage({"chatUserId" : data["chatRoomId"], "messages" : [{"id" : data["id"], "message" : data["message"], "senderId" : data["senderId"], "receiverId" : data["recieverId"],"messageTimeStamp" : data["messageTime"],"userType" : "receiver"}], "type" : "shift"}) )
            
            RealTimeChatHanlder.NotificatioAudio.play().catch((e)=>{console.log(e)})
            

       
         }

         RealTimeChatHanlder.webSocketObject.onclose = ()=>{
            console.log("connection close")
         }
     }

     static send({senderId, recieverId, message, chatRoomId,messageId})
     {
         
         if(RealTimeChatHanlder.webSocketObject.readyState != WebSocket.CLOSED)
         {
            const formatted_data = JSON.stringify({"message" : message, "senderId" : senderId, "receiverId" : recieverId, "chatRoomId": chatRoomId})
            RealTimeChatHanlder.webSocketObject.send(formatted_data)
            // console.log(formatted_data)
            RealTimeChatHanlder.dispatch( addChatMessage({"chatUserId" : chatRoomId, "messages" : [{"id" : messageId, "message" : message, "senderId" : senderId, "receiverId" : recieverId,"messageTimeStamp" : Date.now() / 1000,"userType" : "sender"}], "type" : "shift"}) )
         }

     }

}

