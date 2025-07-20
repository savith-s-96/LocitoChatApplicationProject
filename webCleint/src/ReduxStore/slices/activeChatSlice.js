import { createSlice } from "@reduxjs/toolkit";


const activeChatReducer = createSlice(
    {
        name : "activeChatUser",
        initialState : {
            chatRoomId: null, chatUserId: null, mobileNumber: null, profileImageUrl: null, userName: null
        },
        reducers : 
        {
            changeActiveChatUser : (state, action)=>{ state = action.payload ; return state}
        }
    }
)

export const {changeActiveChatUser} = activeChatReducer.actions
export default activeChatReducer.reducer