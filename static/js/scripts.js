document.addEventListener('DOMContentLoaded', function () {
    // YouTube Video Logic
    const videoContainer = document.getElementById('random-ad-video');
    const videoIds = JSON.parse(videoContainer.dataset.videos); // Get the video list from the data attribute

    let shuffledVideos = [...videoIds].sort(() => Math.random() - 0.5);
    let currentIndex = 0;

    function playVideo(videoId) {
        videoContainer.src = `https://www.youtube.com/embed/${videoId}?autoplay=1&mute=1&enablejsapi=1&rel=0&loop=1&playlist=${shuffledVideos.join(',')}&controls=0&modestbranding=1&showinfo=0`;
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

    // Genre Filtering Logic
    const filters = document.querySelectorAll('.filter');
    const gameCards = document.querySelectorAll('.game-card');

    filters.forEach(filter => {
        filter.addEventListener('click', function (e) {
            e.preventDefault();
            const genre = this.dataset.genre;

            gameCards.forEach(card => {
                if (genre === 'all' || card.dataset.genre === genre) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
});
