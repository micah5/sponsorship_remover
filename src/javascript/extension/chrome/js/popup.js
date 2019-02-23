/**
 * @author Micah Price (98mprice@gmail.com)
 * Logic for ../popup.html
 */

 new Vue({
  el: '#app',
  data: {
    on: false, // whether or not model has been prepared
    id: null, // video id of current video
    predictionResult: null, // object containing prediction vector and section data
    loadingModel: false, // whether or not model is currently being prepared
    tab: null, // current tab
    loadingPrediction: false, // whether or not prediction data is currently being prepared
    blocking: false, // whether or not the sponsor blocker is enabled on the video
    oldVideoId: null // video id from previous session
  },
  /**
   * Initalises everything from previous session, if they exist
   */
  mounted: function () {
    chrome.tabs.query({ "active": true, "lastFocusedWindow": true }, (tabs) => {
      const url = new URL(tabs[0].url)
      this.id = url.searchParams.get("v")
      this.tab = tabs[0]
      chrome.tabs.sendMessage(this.tab.id, { type: "isModelPrepared" },
        (res) => {
          this.on = res
      })
      chrome.tabs.sendMessage(this.tab.id, { type: "isPredictionDone" },
        (res) => {
          this.predictionResult = res
      })
      chrome.tabs.sendMessage(this.tab.id, { type: "isBlocking" },
        (res) => {
          this.blocking = res
      })
      chrome.tabs.sendMessage(this.tab.id, { type: "getVideoId" },
        (res) => {
          this.oldVideoId = res
      })
    })
  },
  computed: {
    /**
     * Creates an array of all the sponsored periods.
     * TODO: Remove this, as it's duplicate code
     * @return {array} Array of start/end times of sponsored periods.
     */
    predictionPretty: function() {
      const predictionPretty = []
      if (this.predictionResult) {
        for (const [idx, section] of this.predictionResult.sections.entries()) {
          if (this.predictionResult.predictions[idx] < 0.5) {
            if (predictionPretty.length >= 1) {
              const lastEntry = predictionPretty[predictionPretty.length - 1]
              if (section.startTime < (lastEntry.endTime + 5)) {
                predictionPretty[predictionPretty.length - 1].endTime = section.endTime
              } else {
                predictionPretty.push({
                  startTime: section.startTime,
                  endTime: section.endTime
                })
              }
            } else {
              predictionPretty.push({
                startTime: section.startTime,
                endTime: section.endTime
              })
            }
          }
        }
      }
      return predictionPretty
    }
  },
  watch: {
    /**
     * Checks every second to see if the model has been prepared yet.
     */
    loadingModel: function() {
      if (this.loadingModel == true) {
        const interval = setInterval(() => {
           chrome.tabs.sendMessage(this.tab.id, { type: "isModelPrepared" },
             (res) => {
               if (res == true) {
                 this.on = true
                 clearInterval(interval)
                 this.loadingModel = false
               }
           })
        }, 1000)
      }
    },
    /**
     * Checks every second to see if the prediction has been done yet.
     */
    loadingPrediction: function() {
      if (this.loadingPrediction == true) {
        const interval = setInterval(() => {
           chrome.tabs.sendMessage(this.tab.id, { type: "isPredictionDone" },
             (res) => {
               if (res) {
                 this.predictionResult = res
                 this.oldVideoId = this.id
                 clearInterval(interval)
                 this.loadingPrediction = false
               }
           })
        }, 1000)
      }
    }
  },
  methods: {
    /**
     * Sends message to start preparing the model.
     */
    prepareModel: function() {
      chrome.tabs.sendMessage(this.tab.id, { type: "prepareModel" },
        (res) => {
          if (res == true) {
            this.loadingModel = true
          }
      })
    },
    /**
     * Opens external link in new tab.
     */
    openLink: function(url) {
      chrome.tabs.create({ url: url })
    },
    /**
     * Sends message to start the prediction.
     */
    startPrediction: function() {
      chrome.tabs.sendMessage(this.tab.id, { type: 'predict', id: this.id },
        (res) => {
          if (res == true) {
            this.loadingPrediction = true
          }
        }
      )
    },
    /**
     * Pretty print time.
     * Taken from: https://stackoverflow.com/questions/3733227/javascript-seconds-to-minutes-and-seconds
     */
    display: function(seconds) {
      const hours = seconds / 3600
      const minutes = (seconds % 3600) / 60
      seconds %= 60

      return [hours, minutes, seconds].map(val => ('0' + Math.floor(val)).slice(-2)).join(':')
    },
    /**
     * Sends message to go to point in video.
     */
    goTo: function(seconds) {
      chrome.tabs.sendMessage(this.tab.id, { type: 'goTo', seconds: seconds },
        (res) => { }
      )
    },
    /**
     * Sends message to turn the sponsorship blocker for the video on or off.
     */
    toggleBlocker: function() {
      chrome.tabs.sendMessage(this.tab.id, { type: 'toggleBlocking' },
        (res) => {
          this.blocking = res
        }
      )
    }
  }
})
