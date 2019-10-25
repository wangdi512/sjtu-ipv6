const list = require("./mock/list.json");
const upload = require("./mock/upload.json");

module.exports = {
  devServer: {
    port: 8080,
    before(app) {
      app.get("/get_all_result", (req, res) => {
        res.json(list);
      });
      app.post("/upload_pcap", (req, res) => {
        res.json(upload);
      });
    }
  },
  css: {
    loaderOptions: {
      sass: {
        prependData: `
          @import "@/assets/global.scss";
        `
      }
    }
  }
};
