import "./Home.css"
import Loader from "../../Component/Loader/Loader"
import { useEffect } from "react"
import { useNavigate } from "react-router-dom"
import { get_access_token } from "../../Hooks/AuthenticationHook";


function Home() {

  const navigate = useNavigate() ; 
 
  useEffect(()=>{

      async function isLoggedIn()
      {
          const data = await get_access_token()
          
          if(data)
          {
             navigate("/chat",{"state" : {"userId" : data["userId"]}})
          }

          else 
          {
             navigate("/login")
          }
      }

      isLoggedIn()
       
  },[])

  return (
    <Loader/>
  )
}

export default Home