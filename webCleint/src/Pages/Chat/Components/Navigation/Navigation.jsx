import React, { useEffect, useState } from 'react'
import "./Navigation.css"
import logo from "../../../../assets/Icons/chat-dots-svgrepo-com.svg"
import userIcon from "../../../../assets/Icons/userDefaultIcon.svg"
import { getUser } from '../../../../Hooks/UserHooks'
import { Host } from '../../../../Hooks/Configuartion'
import { ChangeUserProfile } from '../../../../ReduxStore/slices/userSlice'
import { useDispatch, useSelector } from 'react-redux'
import { memo } from 'react'

function Navigation() {


  // const [userData, setUserData] = useState(null)
  const dispatch = useDispatch()
  const [ProfileContainer, setProfileContainer] = useState(null);
  const userData = useSelector((state)=>{ return state.userProfile })


  useEffect(
    ()=>{

      async function fetchuser(){

        const data = await getUser()
        if(data)
        {

              dispatch(ChangeUserProfile(data))
          
        }

      }

      fetchuser()
      setProfileContainer(document.querySelector(".profile"))
    },[])


    function openProfile()
    {
      if(ProfileContainer)
      {
        ProfileContainer.classList.add("active")
      }
    }

  return (
    <div className="locito-nav-bar">
        <div className="logo">
            <img src={logo} alt="logo-img" />
            <h2>Locito Chat</h2>
        </div>
        <div className="menu" onClick={openProfile}>
            <img src={ userData ? (userData["profileImageUrl"] ? Host +"/user/profile?filePath="+ userData["profileImageUrl"] : userIcon ) : userIcon}  />
        </div>
    </div>
  )
}

export default memo(Navigation)