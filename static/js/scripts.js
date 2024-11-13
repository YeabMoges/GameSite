document.addEventListener('DOMContentLoaded', function () {
    const videoContainer = document.getElementById('random-ad-video');
    const videoIds = JSON.parse(videoContainer.dataset.videos); // Get the video list from the data attribute

    let shuffledVideos = [...videoIds].sort(() => Math.random() - 0.5);
    let currentIndex = 0;

    function playVideo(videoId) {
        videoContainer.src = `https://www.youtube.com/embed/${videoId}?autoplay=1&mute=1&enablejsapi=1&rel=0&loop=1&playlist=${shuffledVideos.join(',')}`;
    }

    function playNextVideo() {
        currentIndex = (currentIndex + 1) % shuffledVideos.length;
        playVideo(shuffledVideos[currentIndex]);
    }

    // Initialize the YouTube API player
    function onYouTubeIframeAPIReady() {
        new YT.Player('random-ad-video', {
            events: {
                'onStateChange': function (event) {
                    if (event.data === YT.PlayerState.ENDED) {
                        playNextVideo();
                    }
                }
            }
        });
    }

    playVideo(shuffledVideos[currentIndex]);

    // Load YouTube IFrame API
    const scriptTag = document.createElement('script');
    scriptTag.src = "https://www.youtube.com/iframe_api";
    document.body.appendChild(scriptTag);

    window.onYouTubeIframeAPIReady = onYouTubeIframeAPIReady;
});
