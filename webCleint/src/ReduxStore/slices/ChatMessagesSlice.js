import { createSlice } from "@reduxjs/toolkit";


const chatMessagesReducer = createSlice(
    {
        name : "chatMessages",
        initialState : {}, 
        reducers : 
        {
            addChatMessage : function (state,action){

                
                //  state[action.payload["chatUserId"]]["messages"].push(action.payload["messages"])
                // console.log(action.payload)
                const chatUserId = action.payload["chatUserId"]
                const messages = action.payload["messages"]

                if(chatUserId && messages.length > 0)
                {
                     
                    if(action.payload["type"] == "shift")
                    {
                      
                        for (let message of messages)
                    {
                          state[chatUserId]["messages"].unshift(message)
                    }

                    }

                    else 
                    {
                     
                        for (let message of messages)
                    {
                          state[chatUserId]["messages"].push(message)
                    }

                    }
                    

                }

                 return state
            },

            addChatUserId : function (state, action)
            {
                if( action.payload["chatUserId"] in state)
                {
                  return state   
                }

                else 
                {
                    state[action.payload["chatUserId"]] = { "messages" : [],"hasMore" : true, "scrollPosition" : null}
                
                    return state
                }
            },

            changeUserChatMessageState : function (state, action) 
            {
                
                state[action.payload["chatRoomId"]][action.payload["stateName"]] = action.payload["stateValue"]
                // console.log(state)
                return  state 
            }
        }
    }
)

export const {addChatMessage, addChatUserId, changeUserChatMessageState} = chatMessagesReducer.actions 
export default chatMessagesReducer.reducer