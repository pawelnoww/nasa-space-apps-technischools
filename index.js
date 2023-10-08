let meteors;
let map;

const searchParams = new URLSearchParams(window.location.search);
const searchResults = document.getElementById("searchResults");
let resultDiv

let isDate = function (input) {
    if (Object.prototype.toString.call(input) === "[object Date]")
        return true;
    return false;
};

function pop(name, id, year, mass, lat, long) {
    let link = 'https://j3rzy.dev/nothing', icon = 'https://meteorclient.com/icon.png'
    if (name == 'Hoba') link='https://pl.wikipedia.org/wiki/Hoba', icon='https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Hoba_Meteorite_sire.jpg/1280px-Hoba_Meteorite_sire.jpg'
    if (name == 'Allende') link='https://pl.wikipedia.org/wiki/Allende_(meteoryt)', icon='https://upload.wikimedia.org/wikipedia/commons/f/f9/AllendeMeteorite.jpg'
    if (name == 'Murchison') link='https://en.wikipedia.org/wiki/Murchison_meteorite', icon='https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Murchison_crop.jpg/800px-Murchison_crop.jpg'
    if (name == 'Campo del Cielo') link='https://pl.wikipedia.org/wiki/Campo_del_Cielo', icon='https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Campo_del_cielo_cat.jpg/800px-Campo_del_cielo_cat.jpg'
    if (name == 'Sikhote-Alin') link='https://pl.wikipedia.org/wiki/Sikhote-Alin', icon='https://upload.wikimedia.org/wikipedia/commons/a/ab/SikhoteAlinMeteorite.jpg'
    return `
    <a href="${link}"><img src="${icon}" , width="250"></a>
    <br><b>${name} (ID${id})</b><br>Discovered in year ${year}
    <br>Weights ${mass}g<br><i>${lat}, ${long}</i>
    `.toString()
}

// Map, markers...
async function main() {
	await fetch("https://data.nasa.gov/api/views/gh4g-9sfh/rows.csv")
    .then(response => response.text())
    .then(async (data) => {
        map = L.map("map").setView([50.56083232165689, 22.05540601449895], 5); // [latitude,longitude], zoom (less, further)

        L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
            attribution:
                '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        }).addTo(map)

        meteors = data.split('\n')
        meteors.splice(0, 1)

        const response = await fetch("https://data.nasa.gov/resource/gh4g-9sfh.json")
        const json = await response.json()

        json.forEach(async meteor => {
            if (meteor.reclat == null || meteor.reclong == null) return // missing position data "For practical purposes, return in a forEach() callback is equivalent to continue in a conventional for loop."
            await L.marker([meteor.reclat, meteor.reclong])
                .addTo(map)
                .bindPopup(pop(meteor.name, meteor.id, dayjs(meteor.year).format("YYYY"), meteor.mass, meteor.reclat, meteor.reclong))
        })

        if (searchParams.get('name')) {
            meteors.forEach(async (m) => {
                if (m.toUpperCase().startsWith(searchParams.get('name').toUpperCase())) {
                    let geolocation = `${m[9]}, ${m[10]}`.replace(/["() ]/g, '').split(',')
                    let name=m[0], id=m[1], year=m[6], mass=m[4]
                    await L.marker([geolocation[0], geolocation[1]])
                        .addTo(map)
                        .bindPopup(pop(name, id, year, mass, geolocation[0], geolocation[1]))
                    map.setView([geolocation[0], geolocation[1]], 13);
                }
            })
        }
    })
}

main()

// Search function
async function search() {
    var input, filter;
    input = document.getElementById("search");
    filter = input.value.toUpperCase();
    //const searchResults = document.getElementById("searchResults");

    const isMenuFolded = !searchResults.classList.contains("show");

    // Clear previous results
    searchResults.innerHTML = '';

    for (let i = 0; i < meteors.length; i++) {
        let regex = new RegExp(input.value);
        if (meteors[i].toUpperCase().startsWith(filter) || regex.test(meteors[i]) /*|| (!isNaN(filter) && meteors[i].split(',')[1] == parseInt(filter))*/) {
            let m = meteors[i].split(',')
            let geolocation = `${m[9]}, ${m[10]}`.replace(/["()]/g, '').split(', ')
            resultDiv = document.createElement("div");
            resultDiv.textContent = `${m[0]}`;
            resultDiv.setAttribute("data-index", i);
            resultDiv.classList.add("result-item");
            resultDiv.addEventListener("click", async function() {
                let geolocation = `${m[9]}, ${m[10]}`.replace(/["() ]/g, '').split(',')
                let name=m[0], id=m[1], year=m[6], mass=m[4]
                if (m[3].includes('"')) {year=m[7], mass=m[5]}
                console.log(year)
                await L.marker([geolocation[0], geolocation[1]])
                    .addTo(map)
                    .bindPopup(pop(name, id, year, mass, geolocation[0], geolocation[1]))
                map.setView([geolocation[0], geolocation[1]], 13);
            });
            resultDiv.addEventListener("contextmenu", function(event) {
                event.preventDefault(); // Prevent the default browser context menu
                console.log('placeholder!')
            });
            searchResults.appendChild(resultDiv);
        }
    }

    // Show or hide the search results menu with animation
    if (filter.length > 0 && isMenuFolded) {
        searchResults.classList.add("show");
    } else {
        searchResults.classList.remove("show");
    }
}

// Clicking and unclicking search result list
document.addEventListener("click", function(event) {
    const searchInput = document.getElementById("search");
    const searchResults = document.getElementById("searchResults");

    if (event.target == searchInput && resultDiv.classList.contains("result-item")) searchResults.classList.add("show");

    if (event.target !== searchInput && event.target !== searchResults) {
        searchResults.classList.remove("show");
    }
});