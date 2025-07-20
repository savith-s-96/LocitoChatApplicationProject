import { Host } from "./Configuartion"
import customHistory from "./customHistory"

export async function get_access_token()
{
    const url = Host + "/user/get/access-token"
    const response = await fetch(url,
        {
            method : "GET",
            credentials : "include"
        }
    )
    if(response.status == 200)
    {
        return await response.json()
    }

    else 
    {
        
        customHistory.push("/login")
        return 
    }
}

export async function login_api({userEmail = null, userMobile = null})
{
    // console.log(userEmail,userMobile)
    if(userEmail && userMobile)
    {
       const url = Host + "/register"
       const response = await fetch(url,{ 
         method : "POST",
         headers : {
             "Content-Type" : "application/json"
         },
         body : JSON.stringify({ "UserEmail" : userEmail, "MobileNumber" : userMobile }),
         credentials : "include"

    })
    // console.log(response)

    if(response.status == 200)
    {
        return await response.json()
    }

    else 
    {
        return await response.json()
    }
    }

    else 
    {
        return {"message" : "Invalid Credentials"}
    }
}


export async function verifyOtp({otp, user_id})
{
  if(otp)
  {
    const url = `${Host}/verify/otp/user?user_id=${user_id}&otp=${otp}` 
    const response = await fetch(url,{method: "GET",
  credentials: "include"}) ;
    const data = await response.json() ;
    if(response.status == 200)
    {
        return data
    }

    else 
    {
        return false
    }
  }
}


export async function resendOtp({user_id})
{
    const url = `${Host}/resend/otp?user_id=${user_id}`
    const response = await fetch(url,{method: "GET",
  credentials: "include"})
    const data = await response.json()
    if( response.status == 200)
    {
        return data 
    }
}


