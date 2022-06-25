window.onscroll = function() { scrollFunction() };

function scrollFunction() {
    if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
        document.querySelector("header").style.height = "10vh";

    } else {
        document.querySelector("header").style.height = "50vh";

    }
}