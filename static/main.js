window.onscroll = function() { scrollFunction() };

function scrollFunction() {
    if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
        document.querySelector("header").style.height = "10vh";

    } else {
        document.querySelector("header").style.height = "50vh";

    }
}


window.addEventListener('load', async() => {
    url = "/"

    let result = await axios.get(`https://api.ipify.org?format=json`, {
        mode: 'cors',
        credentials: 'include'
    });

    let data = await result.data;
    console.log(data)
    let res = axios.post(url, {
            data
        })
        .then((response) => {
            window.location.assign('/' + data.ip);
        }, (error) => {
            console.log(error);
        });
})