import { get_access_token } from "./AuthenticationHook";
import { Host } from "./Configuartion";


export async function getUser() {



    const url = `${Host}/user/profile/details` 
    const response = await fetch(url,{credentials : "include"})
    const data = await response.json()
    
    if(data["access_token"] == "false")
    {
        const token_response = await get_access_token()
        if(token_response)
        {
          return await getUser()
        }

        else
        {
            return false
        }

    }

    else 
    {
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


export async function updateProfile({userName, userProfileImageFile}) {


      const formData = new FormData()

      if(userName)
      {
       formData.append("userName",userName)
      }

      if(userProfileImageFile)
      {
        formData.append("ProfileImage", userProfileImageFile)
      }
      
     
      console.log(formData.get("ProfileImage"))
      
      const url = `${Host}/user/profile/update`

      const response = await fetch(
         url,
         {
            method : "PUT",
            body : formData,
            credentials : "include"
         }
      )

    const data = await response.json()

        
    if(data["access_token"] == "false")
    {
        const token_response = await get_access_token()
        if(token_response)
        {
          return await updateProfile({userName,userProfileImageFile})
        }

        else
        {
            return false
        }

    }

    else 
    {
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