function displayTime(pos) {
    let minutes = Math.floor(pos / 60)
    let sec = pos % 60
    return `${minutes}:${sec}`
}

function createTimingInfo() {
  var timing_p = document.createElement("p")
  timing_p.setAttribute("id", "timing-info")
  return timing_p
}

function clearParent(parent) {
  while (parent.firstChild) {
    parent.removeChild(parent.firstChild)
  }
}

var song = {}
var current_song = new Proxy(song, {
  set: (target, key, value) => {
    target.ref = $("#queue")[0].firstChild
    target[key] = value
    return true
  }
})

setInterval((e) => {
  if (song.cur) {
    song.cur.pos += 1
    if(song.ref) {
      $("#timing-info").text(`${displayTime(Math.floor(song.cur.pos))}/${song.cur.duration}`)
    }
  }
}, 1000)


function displayResults(results) {
    var resultlist = document.getElementById("results")
    clearParent(resultlist)
    results.forEach((res) => {
        let listitem = document.createElement("div")
        let artistname = res.artists[0].name 
        let thumbnail = res.thumbnails[0].url
        let img = document.createElement("img")
        img.setAttribute("src", thumbnail)
        img.setAttribute("class", "result-list")
        img.setAttribute("height", "50px")
        img.setAttribute("width", "50px")
        let title = document.createElement("p")
        title.setAttribute("class", "result-list")
        title.innerHTML = `${artistname} - ${res.title}`
        title.setAttribute("videoId", res.videoId)
        img.setAttribute("videoId", res.videoId)
        listitem.setAttribute("videoId", res.videoId)
        let link = document.createElement("a")
        listitem.appendChild(img)
        listitem.appendChild(title)
        link.appendChild(listitem)
        resultlist.appendChild(link)
        link.addEventListener("click", (e) => {
            console.log(e.target)
            let videoId = e.target.getAttribute("videoId")
            req  = {videoId}
            fetch(`${window.origin}/add`, {
            method: "POST",
            body: JSON.stringify(req)
            })
        })
    })
}


let qinfo_url = location.port != '' ?  `${window.location.hostname}:${location.port}` : `${window.location.hostname}`
const socket = new WebSocket(`ws://${qinfo_url}/qinfo`)


socket.addEventListener("open", (event) => {
  console.log("socket open")
})

setInterval((socket) => {
  socket.send("inquire")
}, 5000, socket)


socket.addEventListener("message", (event) => {
    console.debug("Message from server ", event.data);
    var qdiv = document.getElementById("queue")
    var cur_timing_text = null;
    var qdata = JSON.parse(event.data)
    if (current_song.ref) {
      cur_timing_text = document.getElementById("timing-info").textContent
    }
    clearParent(qdiv)
    qdata.forEach((res, i) => {
      let elm = document.createElement("div")
      elm.setAttribute("pos", i)
      elm.innerText = `${res.artists[0].name} - ${res.title}\n Requested by: ${res.requestor}`
      if (i === 0 && current_song.ref){
        let new_timing = createTimingInfo()
        new_timing.innerText = cur_timing_text
        elm.appendChild(new_timing)
      }
      qdiv.appendChild(elm)
    })
    if (qdata.length > 0) {
      console.debug("queuedata", qdata[0])
      current_song.cur = qdata[0]
      current_song.ref = $("#queue")[0].firstChild
      if ($("#timing-info").length === 0) {
        var timing_p = document.createElement("p")
        timing_p.setAttribute("id", "timing-info")
        current_song.ref.appendChild(timing_p)
      }
      $(function() {
        if (Cookies.get("authenticated") == "1" && window.location.pathname === "/admin") 
          makeRemoveable()
      });
      $("a.removeable").on("click", function(e) {
        e.preventDefault()
        let pos = e.target.children[0].pos
        fetch(`${window.origin}/remove/${pos}`, {
          method: "post"
        })
      })
    } else {
      current_song.cur = null
      current_song.ref = null 
    }
  })
