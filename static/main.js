window.onload = function() {
    let app = new Vue({
        el: "#app",
        data: {
            mood: "",
            error: "",
            playlistReturned: false,
            playlistId: undefined
        },
        computed: {
            code: function() {
                return window.location.href.split("?code=")[1].split("&")[0];
            },
            playlistURL: function() {
                return "https://open.spotify.com/embed/playlist/" + this.playlistId;
            } 
        },
        methods: {
            make_playlist: function() {
                if (this.mood.length == 0) {
                    this.error = "Please select a mood";
                } else {
                    this.playlistReturned = true;
                    this.playlistId = response.playlistId;
                    /*
                    this.error = ""
                    let that = this;
                    var url = 'http://localhost:';
                    fetch(url, {
                        method: 'POST', // or 'PUT'
                        body: JSON.stringify({
                            token: this.code
                        }),
                        headers:{
                            'Content-Type': 'application/json'
                        }
                    }).then(res => res.json())
                        .then(response => {
                            that.playlistReturned = true;
                            that.playlistId = response.playlistId;
                        }).catch(err => {
                            that.error = "unable to create playlist";
                        });
                        */
                } 
            }
        }
    })
}