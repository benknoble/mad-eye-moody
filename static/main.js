window.onload = function() {
    let app = new Vue({
        el: "#app",
        data: {
            message: "Hello, world!"
        },
        computed: {
            code: function() {
                return window.location.href.split("?code=")[1].split("&")[0]
            }
        }
    })
}