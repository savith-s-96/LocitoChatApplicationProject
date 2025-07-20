import { configureStore } from "@reduxjs/toolkit";
import userReducer from "./slices/userSlice" ;
import activeChatUserReducer from "./slices/activeChatSlice";
import chatMessageReducer from "./slices/ChatMessagesSlice" ;

const store = configureStore({
       reducer :
       {
           userProfile : userReducer,
           activeChat : activeChatUserReducer ,
           chatUserMessages : chatMessageReducer 
       }
})


export default store