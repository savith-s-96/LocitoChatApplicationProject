import React, { memo, useEffect, useRef, useState } from 'react'
import "./Profile.css"
import leftArrowIcon from "../../assets/Icons/leftArrowIcon.svg"
import userIcon from "../../assets/Icons/userDefaultIcon.svg"
import { useDispatch } from 'react-redux'
import { useSelector } from 'react-redux'
import { Host } from '../../Hooks/Configuartion'
import { updateProfile } from '../../Hooks/UserHooks'
import { ChangeUserProfile } from '../../ReduxStore/slices/userSlice'


function Profile() {


  const [userName, setUserName] = useState("")
  const [userProfileImageUrl, setUserProfileImageUrl] = useState("")
  const [userProfileImageFile, setUserProfileImageFile] = useState(null)
  const dispatch = useDispatch()
  const ProfileContainer = useRef()

  const userData = useSelector((state)=> { return state.userProfile })

  useEffect(()=>{

      
       const fileInputElement = document.querySelector("#file-input") ;

       document.querySelector("#profile-image-select").addEventListener("click",()=>{

                 fileInputElement.click()
       })

  },[])


  useEffect(()=>{

      if(userData["userName"])
      {
            setUserName(userData["userName"])
      }

      if(userData["profileImageUrl"])
      {
          const profileImageUrl = `${Host}/user/profile?filePath=${userData["profileImageUrl"]}`
          setUserProfileImageUrl(profileImageUrl)

      }

  },[userData])

  
  function InputOnchangHandler(e)
  {
   setUserName(e.target.value)   
  }

  function FileHandler(e)
  {
      setUserProfileImageFile(e.target.files[0])
      setUserProfileImageUrl(URL.createObjectURL(e.target.files[0]))
  }

  async function SubmitHandler(e)
  {
      e.preventDefault()
      const loader = document.querySelector(".loader-green-hr")
      loader.classList.add("active")
      const formattedData = {}
      if(userName)
      {
            formattedData["userName"] = userName
      }

      if(userProfileImageFile)
      {
            formattedData["userProfileImageFile"] = userProfileImageFile
      }
      
      if(Object.keys(formattedData).length > 0)
      {

             const data = await updateProfile(formattedData)
             
             if(data)
             {
                dispatch(ChangeUserProfile(data))
                loader.classList.remove("active")
                
             }

             else 
             {
                  return
             }
      }


      else 
      {
            return
      }
  }

  function closeProfile()
  {
        if(ProfileContainer.current)
        {
            ProfileContainer.current.classList.remove("active")
        }
  }

  return (
    
     <div className="profile" ref={ProfileContainer}>
           <div className="header" style={{backgroundColor:"var(--logo-color)"}}>
             <div className="icon" onClick={closeProfile}>
                <img src={leftArrowIcon} alt="icon" />
             </div>
                 <h1>Profile</h1>
           </div>

           <div className='profile-image-name'>
                 <img id='profile-image-select'  src={userProfileImageUrl ? userProfileImageUrl : userIcon} alt="profile-image" />
                 <input type="file" accept='image/*' hidden id="file-input" onChange={FileHandler} />
                 <input type="text" value={ userName ? userName : ''} placeholder='User Name' onChange={InputOnchangHandler}  />
           </div>
           <div className='edit-btn'>
                <button onClick={SubmitHandler}>Submit</button>
           </div>
     </div>

  )
}

export default memo( Profile )