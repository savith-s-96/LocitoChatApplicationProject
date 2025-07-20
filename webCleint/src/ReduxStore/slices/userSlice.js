import { createSlice } from "@reduxjs/toolkit";


const userReducer = createSlice(
    {
        name :"userProfileData",
        initialState : 
        {
            profileImageUrl : "",
            userName : "",
        },

        reducers :
        {
           ChangeUserProfile : function ChangeUserProfileData(state, action)
            {
                      state = {...state, ...action.payload}

                      return state
            }
        }
    }
)


export const {ChangeUserProfile} = userReducer.actions 
export default userReducer.reducer