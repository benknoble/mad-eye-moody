window.onload = function() {
    let app = new Vue({
        el: "#app",
        data: {
            mood: "",
            error: "",
            playlistName: "",
            playlistReturned: false,
            playlistId: undefined,
            loading: false,
            token: undefined
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
                    this.loading = true;
                    this.error = ""
                    let that = this;
                    var url = '/playlists';
                    fetch(url, {
                        method: 'POST',
                        body: JSON.stringify({
                            code: this.code,
                            token: this.token,
                            mood: this.mood,
                            name: this.playlistName
                        }),
                        headers:{
                            'Content-Type': 'application/json'
                        }
                    }).then(res => res.json())
                        .then(response => {
                            that.playlistReturned = true;
                            that.playlistId = response.playlist_id;
                            that.loading = false;
                            that.token = response.token;
                        }).catch(err => {
                            console.error(err);
                            that.error = "There was an error processing your request. Please try again.";
                            that.loading = false;
                        });
                } 
            }
        }
    })
}
