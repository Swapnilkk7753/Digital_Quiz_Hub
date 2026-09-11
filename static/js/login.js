function log()
{
  email=document.getElementById("emai").value
    passw=document.getElementById("pas").value

fetch(`/Login_sta/${email}/${passw}`,{method:"POST"})
.then(res=>res.json())
.then(data=>{
   if (data.sta==0)
   {
    alert(data.mess)
  window.location.href=data.url
   }
})
.catch(err=>console.error(err))
}