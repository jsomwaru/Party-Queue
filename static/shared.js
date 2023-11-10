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

form.addEventListener("submit", sendData)
const socket = new WebSocket(`ws://${window.location.hostname}/qinfo`)

socket.addEventListener("open", (event) => {
  console.log("socket open")
})
