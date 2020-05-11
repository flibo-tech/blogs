import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

var my_store = JSON.parse(localStorage.getItem("my_store"));

if (my_store) {
  try {
    if (typeof my_store.blog_host == "undefined") {
      localStorage.clear();
      window.location = "/";
    }
  } catch (err) {
    localStorage.clear();
    window.location = "/";
  }
}

export const store = new Vuex.Store({
  state: {
    guest_id: my_store ? my_store.guest_id : null,
    guest_country: my_store ? my_store.guest_country : null,
    app_host: "https://yzal-dev.flibo.ai/",
    api_host: "https://yzal-dev-app.flibo.ai/",
    blog_host: "https://blog.flibo.ai",
    country_mappings: {
      AU: "Australia",
      BR: "Brazil",
      CA: "Canada",
      FR: "France",
      DE: "Germany",
      IN: "India",
      ID: "Indonesia",
      IT: "Italy",
      JP: "Japan",
      MX: "Mexico",
      PH: "Philippines",
      RU: "Russia",
      ES: "Spain",
      GB: "United Kingdom",
      US: "United States",
    },
  },
});
