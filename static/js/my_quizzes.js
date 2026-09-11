/* VIEW RESULT */
function viewResult(qui,cat) {
  alert("Opening result for: " + qui);
 // fetch(`/View_Result/${qui}/${cat}`,{method:"POST"})


  // Later:
  window.location.href = "/View_Result?cat="+cat+"&qui="+qui;
}
