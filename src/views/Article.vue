<template>
  <div v-if="article_raw" v-html="article_raw" />
  <div v-else-if="article_raw == null" id="article_container">
    <ArticleOnDemand />
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "Article",
  components: {
    ArticleOnDemand: () =>
      import(
        /* webpackChunkName: "ArticleOnDemand" */ "../components/ArticleOnDemand.vue"
      )
  },
  data: function() {
    return {
      dialog: false, // for popup
      fliboAd: "flibo-ad.png", // FLIBO AD image
      store: this.$store.state,
      is_mobile: window.screen.height > window.screen.width,
      content_name: null,
      is_movie: false,
      is_show: false,
      content_id: null,
      title: null,
      poster: null,
      main_artists: [],
      release_year: null,
      similar_contents: [],
      where_to_watch: {},
      play_trailer_index: null,
      play_trailer: false,
      lazyloadImages: [],
      lazyloadThrottleTimeout: null
    };
  },
  props: {
    article_raw: {
      default: null
    }
  },
  methods: {
    playTrailer(index) {
      this.play_trailer_index = index;
      this.play_trailer = true;
    },
    goToPlatform(link) {
      window.open(link);
    },
    lazyload() {
      var self = this;
      if (self.lazyloadImages.length == 0) {
        self.lazyloadImages = document.querySelectorAll("img.lazy");
      }
      if (self.lazyloadThrottleTimeout) {
        clearTimeout(self.lazyloadThrottleTimeout);
      }

      self.lazyloadThrottleTimeout = setTimeout(function() {
        var scrollTop = window.pageYOffset;
        self.lazyloadImages.forEach(function(img) {
          if (img.y - 200 < window.innerHeight) {
            img.src = img.dataset.src;
            img.classList.remove("lazy");
            self.lazyloadImages = document.querySelectorAll("img.lazy");
          }
        });
        if (self.lazyloadImages.length == 0) {
          document.removeEventListener("scroll", self.lazyload);
        }
      }, 20);
    }
  },
  mounted() {
    document.addEventListener("scroll", this.lazyload);
  },
  beforeDestroy() {
    document.removeEventListener("scroll", this.lazyload);
  }
};
</script>

<style lang="scss" scoped>
ol {
  list-style: none;
  counter-reset: article-counter;
  //   columns: 2;
  //   -webkit-columns: 2;
  //   -moz-columns: 2;
}
ol li {
  position: relative;
  padding-left: 25px;
  counter-increment: article-counter;
  margin: 25px 0;
}
ol li::before {
  display: inline-block;
  content: counter(article-counter);
  position: absolute;
  width: 40px;
  height: 40px;
  text-align: center;
  padding: 1px;
  font-size: 1.6rem;
  font-weight: bold;
  top: -8px;
  left: -25px;
  border-radius: 50%;
  background-color: #e8e8e8;
}

ol.movie-list {
  padding-left: 0;
}
ol.movie-list li {
  padding-left: 0px;
}

ol.movie-list li::before {
  display: inline-block;
  content: counter(article-counter);
  position: absolute;
  width: 40px;
  height: 40px;
  text-align: center;
  padding: 1px;
  font-size: 1.6rem;
  font-weight: bold;
  top: 22px;
  left: 10px;
  border-radius: 50%;
  background-color: #e8e8e8;
  z-index: 2;
}

.blog-black-background {
  position: fixed;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.75);
  display: table;
  top: 0%;
  left: 0%;
  z-index: 100000;
}
.blog-youtube-player-header {
  position: fixed;
  top: calc(50vh - 28.125vw - 20vh - 25px);
  left: 10px;
  z-index: 100001;
  white-space: initial;
  font-size: 25px;
  font-weight: bold;
  font-style: normal;
  font-stretch: normal;
  line-height: 1.05;
  letter-spacing: normal;
  text-align: center;
  color: #ffffff;
}
.blog-youtube-player-loader {
  border: 10px solid #f3f3f3;
  border-top: 10px solid #3498db;
  border-radius: 50%;
  width: 14vw;
  height: 14vw;
  animation: spin 2s linear infinite;
  position: fixed;
  top: calc(50vh - 20vh - 7vw);
  left: calc(50% - 7vw);
  z-index: 100000;
}
.desktop-blog-youtube-player-loader {
  border: 10px solid #f3f3f3;
  border-top: 10px solid #3498db;
  border-radius: 50%;
  width: 75px;
  height: 75px;
  animation: spin 2s linear infinite;
  position: fixed;
  top: 312.5px;
  left: calc(50vw - 37.5px);
  z-index: 100000;
}
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.blog-youtube-player {
  position: fixed;
  width: 100vw;
  height: 56.25vw;
  top: calc(50vh - 28.125vw - 20vh);
  left: 0;
  z-index: 100001;
}
.blog-youtube-player-platforms {
  display: inline-flex;
  overflow: scroll;
  max-width: 100%;
}
.blog-youtube-player-platform-cropper {
  width: 50px;
  height: 50px;
  position: relative;
  overflow: hidden;
  border-radius: 20%;
}
.blog-youtube-player-platform-icon {
  display: inline-block;
  position: absolute;
  width: 100%;
  margin-left: -50%;
}
.blog-youtube-player-platforms-container {
  display: inline-block;
  vertical-align: top;
  text-align: center;
  margin: 20px 10px 0px 10px;
  cursor: pointer;
  -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
  -webkit-tap-highlight-color: transparent;
}
.blog-tap-to-watch-text {
  white-space: nowrap;
  font-size: 20px;
  font-weight: bold;
  font-style: normal;
  font-stretch: normal;
  line-height: 1.05;
  letter-spacing: normal;
  text-align: center;
  color: #333333;
}
.blog-youtube-player-streaming-box {
  position: fixed;
  bottom: 150px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 100001;
  background-color: #ffffff;
  border-radius: 7px;
  padding: 10px;
  max-width: 95vw;
  text-align: center;
}
::-webkit-scrollbar {
  display: none;
}
.article-poster {
  width: 100%;
  max-width: 500px;
}
.article-similar-container {
  max-width: 800px;
  margin: 0 auto;
}
.videoWrapper {
  position: relative;
  /* padding-bottom: 56.25%; /* 16:9 */
  padding-bottom: 60.25%; /*  */
  padding-top: 25px;
  height: 0;
  background-color: #ddd;
}
.videoWrapper iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.movie-content {
  padding-left: 20px;
}

.article-movie-poster {
  border-radius: 21px;
}

.flibo-ad img {
  width: 100%;
}

@media (max-width: 720px) {
  .movie-content {
    padding-left: 0px;
  }
  .movie-poster-small {
    text-align: left;
    padding-right: 80px !important;
  }

  .flibo-ad img {
    // width: calc(100% + 48px);
    // position: relative;
    // left: -24px;
  }
}
</style>
