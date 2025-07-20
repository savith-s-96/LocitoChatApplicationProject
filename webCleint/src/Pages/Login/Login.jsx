import React, { useEffect, useState } from 'react'
import "./Login.css"
import ChatIcon from "../../assets/Icons/chat-dots-svgrepo-com.svg"
import { login_api, resendOtp, verifyOtp} from '../../Hooks/AuthenticationHook';
import { useNavigate } from 'react-router-dom';

let user_id = null ;
// let inputElements = null ;


async function OtpInputsHandler({navigate})
{
     
     const inputElements = document.querySelectorAll(".otp-inputs input") ;
     document.querySelector(".otp.submit-btn .btn").addEventListener("click",otpVerificationHandler)
     async function otpVerificationHandler(e)
    {
      e.preventDefault() ;
      let otp = ""
      const loader = document.querySelector(".loader-green-hr")
      loader.classList.add("active")
      inputElements.forEach((element,index)=>{
        
          if(element.value != "")
          {
              otp = otp + element.value ;
              element.classList.remove("invalid") ;
          }

          else 
          {
            element.classList.add("invalid") ;
            otp = "" 
          }

      })

      if(otp.length == 6)
      {
        const data = await verifyOtp({otp,user_id})

        if(data["verified"] == "true")
        {
           navigate("/chat", {state : {"userId" : user_id}});
        }
        else 
        {
           console.log(data)
        }
        }
      
        loader.classList.remove("active")
    }


     inputElements.forEach((element,index)=>{

       element.addEventListener("keydown",(e)=>{
          
          const prevIndex = index - 1

          if(e.key == "Backspace") 
          {
                e.preventDefault()
                e.target.value = ""
                if(prevIndex >= 0)
                {
                   inputElements[prevIndex].focus() ;
                }
             

          }

          else 
          {
            console.log("key pressed")
            console.log(e.target.value)
              if(e.target.value != "")
           {

             let nextIndex = index + 1 ;
             if(nextIndex < inputElements.length)
             {
              const nextInput = inputElements[nextIndex] ;
              nextInput.disabled = false ;
              nextInput.focus() ;
             }
            
           }
          }

       })


     })
}


async function resendOtpHandler(e)
{
   e.preventDefault()
   const loader = document.querySelector(".loader-green-hr")
   loader.classList.add("active")
   const data = await resendOtp({user_id})
   const resendMessageElement =  document.querySelector(".msg.resend p")
   if(data["success"] ==  "false")
   {
    resendMessageElement.innerText = data["message"] 
   }

   else 
   {
    resendMessageElement.innerText = "otp resended successfully"
    loader.classList.remove("active")
   }
}

function OtpVerification({data})
{
  const navigate = useNavigate() ;


  useEffect( ()=>{
        OtpInputsHandler({navigate})
  },[] )

  return (
     <div className="otp-verify-page">
        <div className="login-otp-form">
           <p className='otp-email-message'>{data}</p>
           <div className="otp-inputs">
             <input type="tel" maxLength={1} />
             <input type="tel" maxLength={1}/>
             <input type="tel" maxLength={1}/>
             <input type="tel" maxLength={1}/>
             <input type="tel" maxLength={1}/>
             <input type="tel" maxLength={1}/>
           </div>
           <div className="msg resend">
               <p>please resend after message expired</p>
             </div>
           <div className="otp submit-btn resent-btn">
             <button className='btn'>Verify</button>
             <button className='btn' onClick={resendOtpHandler}>resend</button>
           </div>
        </div>
     </div>
  )
}


function LoginPage({setOtpSended, setOtpEmailMessage})
{

async function LoginHandler(e)
{
  e.preventDefault() ;
  const loader = document.querySelector(".loader-green-hr")
  loader.classList.add("active")
  const userEmail = document.querySelector("#user-email-input").value ;
  const userMobile = document.querySelector("#user-mobile-input").value ;
  const data = await login_api({userEmail,userMobile}) ;
  if(data["success"] == "true")
  {
    document.querySelector(".error-msg p").innerText = "";
    setOtpEmailMessage(data["message"]) ;
    user_id = data["user_id"];
    setOtpSended(true) ;
    loader.classList.remove("active")
  }

  else 
  {
    document.querySelector(".error-msg p").innerText = data["message"] ;
  }
}

   useEffect(()=>{

      document.querySelector(".btn.login-btn").addEventListener("click",LoginHandler) 

 },[])


  return (
    <div className="login-page">
         <div className="login-form">
            <div className="logo">
                <img src={ChatIcon} alt="logo" />
                <h2>Locito Chat</h2>
            </div>
            <div className="user-email-and-mobile-number">
                 <input type="text" id='user-email-input' placeholder='Enter Email' required />
                 <input type="text" id="user-mobile-input" placeholder='Enter Mobile'  required/>
            </div>
            <div className="error-msg">
              <p></p>
            </div>
            <div className="login-btn">
                <button className='btn login-btn' >Log In</button>
            </div>
         </div>
    </div>
  )
}




function Login() {


 const [isOtpSended, setOtpSended] = useState(false) ; 
 const [otpEmailMessage,setOtpEmailMessage] = useState(null) ;
 





  return (

     <>
       {
       isOtpSended ? <OtpVerification data={otpEmailMessage}/> : <LoginPage setOtpSended={setOtpSended} setOtpEmailMessage={setOtpEmailMessage} />
       }
     </>  
    

  )
}

export default Login