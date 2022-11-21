// $('#btn-select').click(function () {
//     console.log("click")
//     /ticket/?username=
// });

// var scrt_var = Quagmire; 
// openPage = function() {
// location.href = "/ticket/?username="+scrt_var;
// }

(function() {
    var scrt_var = "Quagmire";
    var strLink = "/ticket/?username=" + scrt_var;
    document.getElementById("btn-select").setAttribute("href",strLink);
})();