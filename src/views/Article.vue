<template>
  <div>
    <section class="container" v-if="title">
      <div class="row">
        <div class="col-12">
          <v-breadcrumbs :items="navigation_links"></v-breadcrumbs>
          <v-img
            class="article-movie-poster"
            :src="poster.replace('/w500/', '/w1280/')"
            alt=""
            aspect-ratio="2"
          ></v-img>
        </div>
      </div>

      <div class="row">
        <div class="col-12">
          <div class="article-similar-container">
            <h1>
              Top {{ similar_contents.length }} awesome
              {{ is_movie ? "movies" : "shows" }} like {{ title }} that you will
              enjoy watching
            </h1>

            <p>
              You just finished watching {{ title }} and you can't get over how
              good this {{ is_movie ? "movie" : "show" }} was. Now you want to
              watch more of such masterpieces. We have curated a list of similar
              {{ is_movie ? "movies" : "shows" }} which are created by the likes
              of
              <span v-if="main_artists.length == 3"
                >{{ main_artists[0] }}, {{ main_artists[1] }} and
                {{ main_artists[2] }}</span
              >
              <span v-if="main_artists.length == 2"
                >{{ main_artists[0] }} and {{ main_artists[1] }}</span
              >
              <span v-if="main_artists.length == 1">{{ main_artists[0] }}</span>
              . Here goes the list -
            </p>

            <ol>
              <div class="row">
                <div class="col-6">
                  <li
                    v-for="(item, index) in similar_contents.slice(0, 5)"
                    :key="index"
                  >
                    {{ item.title }}
                  </li>
                </div>

                <div class="col-6">
                  <li
                    v-for="(item, index) in similar_contents.slice(5)"
                    :key="index"
                  >
                    {{ item.title }}
                  </li>
                </div>
              </div>
            </ol>

            <ol class="movie-list">
              <li v-for="(item, index) in similar_contents" :key="index">
                <div class="row">
                  <div class="col-md-6">
                    <img
                      class="article-poster"
                      :src="item.poster"
                      :alt="item.title"
                    />
                  </div>

                  <!-- MOVIE CONTENT -->
                  <div class="col-md-6">
                    <div class="movie-content">
                      <h2>
                        <a
                          style="color: #333;text-decoration: none;"
                          :href="
                            store.app_host +
                              'content/' +
                              item.content_id +
                              '/' +
                              item.title
                                .replace(/[^a-z0-9]+/gi, '-')
                                .toLowerCase()
                          "
                          target="_blank"
                          >{{ item.title }}</a
                        >
                      </h2>

                      <!--  -->
                      <p>{{ item.summary_text }}</p>
                      <!--  -->
                      <p
                        v-if="
                          Object.keys(where_to_watch).length &&
                            where_to_watch[JSON.stringify(item.content_id)]
                              .streaming_info
                        "
                      >
                        <span style="white-space: pre-wrap;"
                          >You can watch this on
                        </span>
                        <span
                          v-for="(streaming_item,
                          streaming_index) in where_to_watch[
                            JSON.stringify(item.content_id)
                          ].streaming_info"
                          :key="streaming_index"
                        >
                          <span
                            style="white-space: pre-wrap;"
                            v-if="
                              Object.keys(
                                where_to_watch[JSON.stringify(item.content_id)]
                                  .streaming_info
                              ).indexOf(streaming_index) ==
                                Object.keys(
                                  where_to_watch[
                                    JSON.stringify(item.content_id)
                                  ].streaming_info
                                ).length -
                                  1 &&
                                Object.keys(
                                  where_to_watch[
                                    JSON.stringify(item.content_id)
                                  ].streaming_info
                                ).indexOf(streaming_index) != 0
                            "
                          >
                            and
                          </span>

                          <span
                            v-else-if="
                              Object.keys(
                                where_to_watch[JSON.stringify(item.content_id)]
                                  .streaming_info
                              ).indexOf(streaming_index) != 0
                            "
                            >,
                          </span>

                          <a
                            style="font-weight: bold;color: #333;text-decoration: none;"
                            :href="streaming_item"
                            target="_blank"
                            >{{
                              streaming_index
                                .replace(/[_]+/gi, " ")
                                .replace(/(^|\s)\S/g, function(t) {
                                  return t.toUpperCase();
                                })
                            }}
                          </a>
                        </span>
                        .
                      </p>
                      <!-- TRAILER -->
                      <v-btn
                        v-if="item.youtube_trailer_id"
                        @click="
                          item.youtube_trailer_id ? playTrailer(index) : null
                        "
                      >
                        Watch Trailer
                      </v-btn>
                      <!--  -->
                    </div>
                  </div>
                </div>
              </li>
            </ol>
          </div>
          <!--  -->
        </div>
        <!--  -->
      </div>
    </section>

    <transition
      appear
      enter-active-class="animated fadeIn"
      leave-active-class="animated fadeOut"
    >
      <div>
        <div
          class="blog-black-background"
          v-if="play_trailer"
          @click="play_trailer = !play_trailer"
        />

        <div
          class="blog-youtube-player-header"
          style="'top: 75px;left: calc(50vw - 500px);'"
          v-if="play_trailer"
        >
          Trailer
        </div>

        <div v-if="play_trailer" class="blog-youtube-player-loader" />

        <iframe
          class="blog-youtube-player"
          style="width: 1000px;left: calc(50vw - 500px);top: 100px;height: 500px;"
          v-if="play_trailer"
          type="text/html"
          :src="
            'https://www.youtube.com/embed/' +
              similar_contents[play_trailer_index].youtube_trailer_id +
              '?autoplay=1'
          "
          frameborder="0"
          allowfullscreen
        />

        <!-- <div v-if="play_trailer" class="videoWrapper">
							<iframe
              v-if="play_trailer"
								:src="'https://www.youtube.com/embed/' +
              similar_contents[play_trailer_index].youtube_trailer_id"
								frameborder="0"
								allow="autoplay; fullscreen"
								allowfullscreen
							></iframe>
						</div> -->

        <div
          class="blog-youtube-player-streaming-box"
          v-if="
            play_trailer &&
              Object.keys(where_to_watch).length &&
              where_to_watch[
                JSON.stringify(similar_contents[play_trailer_index].content_id)
              ].streaming_info
          "
        >
          <div class="blog-tap-to-watch-text">
            {{ is_mobile ? "Tap to watch on" : "Click to watch on" }}
          </div>

          <div
            class="blog-youtube-player-platforms"
            v-if="
              where_to_watch[
                JSON.stringify(similar_contents[play_trailer_index].content_id)
              ].streaming_info
            "
          >
            <div
              class="blog-youtube-player-platforms-container"
              v-for="(item, index) in where_to_watch[
                JSON.stringify(similar_contents[play_trailer_index].content_id)
              ].streaming_info"
              :key="index"
            >
              <div
                @click="goToPlatform(item)"
                class="blog-youtube-player-platform-cropper"
              >
                <img
                  v-bind:src="
                    'https://flibo-images.s3-us-west-2.amazonaws.com/logos/platforms/' +
                      index +
                      '.jpg'
                  "
                  class="blog-youtube-player-platform-icon"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import axios from "axios";
import { mixin as onClickOutside } from "vue-on-click-outside";
export default {
  name: "Article",
  mixins: [onClickOutside],
  metaInfo() {
    if (this.title) {
      return {
        title: this.meta_title,
        meta: [
          {
            vmid: "description",
            name: "description",
            content: this.meta_description
          },
          {
            vmid: "og:title",
            property: "og:title",
            content: this.meta_title
          },
          {
            vmid: "og:description",
            property: "og:description",
            content: this.meta_description
          },
          {
            vmid: "og:image",
            property: "og:image",
            content: this.poster.replace("/w500/", "/w1280/")
          },
          {
            vmid: "twitter:title",
            name: "twitter:title",
            content: this.meta_title
          },
          {
            vmid: "twitter:description",
            name: "twitter:description",
            content: this.meta_description
          },
          {
            vmid: "twitter:image",
            name: "twitter:image",
            content: this.poster.replace("/w500/", "/w1280/")
          }
        ]
      };
    }
  },
  data: function() {
    return {
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
      play_trailer: false
    };
  },
  created() {
    var self = this;
    this.content_name = this.$route.params.content_name_piece
      .replace("movies-like-", "")
      .replace("shows-like-", "");
    this.is_movie = this.$route.params.content_name_piece.startsWith(
      "movies-like-"
    );
    this.is_show = this.$route.params.content_name_piece.startsWith(
      "shows-like-"
    );
    axios
      .post(self.$store.state.api_host + "similar_contents_for_blog", {
        content_name: self.content_name,
        content_type: self.is_movie ? "movie" : "tv",
        guest_id: self.$store.state.guest_id
      })
      .then(function(response) {
        if (response.status == 200) {
          self.content_id = response.data.content_id;
          self.title = response.data.title;
          self.poster = response.data.poster;
          self.main_artists = response.data.main_artists;
          self.release_year = response.data.release_year;
          self.similar_contents = response.data.similar_contents;

          var content_ids = [];
          var x;
          for (x in self.similar_contents) {
            content_ids.push(self.similar_contents[x].content_id);
          }
          if (self.$store.state.guest_country != null) {
            axios
              .post(
                self.$store.state.api_host + "where_to_watch_similar_content",
                {
                  content_ids: content_ids,
                  country: self.$store.state.guest_country
                }
              )
              .then(function(response) {
                if (response.status == 200) {
                  self.where_to_watch = response.data;
                  document.dispatchEvent(new Event("x-app-rendered"));
                } else {
                  document.dispatchEvent(new Event("x-app-rendered"));
                }
              });
          } else {
            setTimeout(
              axios
                .post(
                  self.$store.state.api_host + "where_to_watch_similar_content",
                  {
                    content_ids: content_ids,
                    country: self.$store.state.guest_country || "United States"
                  }
                )
                .then(function(response) {
                  if (response.status == 200) {
                    self.where_to_watch = response.data;
                    document.dispatchEvent(new Event("x-app-rendered"));
                  } else {
                    document.dispatchEvent(new Event("x-app-rendered"));
                  }
                }),
              500
            );
          }
        }
      })
      .catch(function(error) {
        // console.log(error);
      });
  },
  computed: {
    navigation_links: function() {
      var crumbs = [
        {
          text: "Home",
          disabled: false,
          href: "/"
        },
        {
          text: (this.is_movie ? "Movies" : "Shows") + " like " + this.title,
          disabled: true,
          href: this.$route.path
        }
      ];
      return crumbs;
    },
    meta_title: function() {
      return (
        "Top " +
        this.similar_contents.length +
        " awesome " +
        (this.is_movie ? "movies" : "shows") +
        " like " +
        this.title +
        " that you will enjoy watching"
      );
    },
    meta_description: function() {
      return (
        "Are you looking for " +
        (this.is_movie ? "movies" : "shows") +
        " like " +
        this.title +
        "? If yes, then we have curated a list for you, a list of " +
        (this.is_movie ? "movies" : "shows") +
        " by the likes of " +
        [
          this.main_artists.slice(0, -1).join(", "),
          this.main_artists.slice(-1)[0]
        ].join(this.main_artists.length < 2 ? "" : " and ") +
        "."
      );
    }
  },
  methods: {
    playTrailer(index) {
      this.play_trailer_index = index;
      this.play_trailer = true;
    },
    goToPlatform(link) {
      window.open(link);
    }
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
  top: 70px;
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
  top: 650px;
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

@media (max-width: 720px) {
  .movie-content {
    padding-left: 0px;
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
}
</style>
