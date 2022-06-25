window.onscroll = function() { scrollFunction() };

function scrollFunction() {
    if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
        document.querySelector("header").style.height = "10vh";

    } else {
        document.querySelector("header").style.height = "50vh";

    }
}

// window.onload = function() {
//     let result = await axios.get(`https://api.ipify.org?format=json`, {
//         mode: 'cors',
//         credentials: 'include'
//     });

//     let data = await result.data;
//     document.getElementById('hide').value = data.ip
//     console.log(data.ip)
//     console.log(document.getElementById('hide').value)
// }