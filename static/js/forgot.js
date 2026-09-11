function forgot()
{
  email=document.getElementById("em1").value
    p=document.getElementById("p").value
        cp=document.getElementById("cp").value


fetch(`/forgot_sta/${email}/${p}/${cp}`,{method:"POST"})
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