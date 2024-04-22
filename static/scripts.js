let selectedMangaId = null;


function show_description(element_id) {
    var description_box = document.getElementById(element_id);
    if (description_box.style.display === "none") {
        description_box.style.display = "block";
    } else{
        description_box.style.display = "none";
       }
    }

function show_add_manga() {
    var manga_search_box = document.getElementById("add_manga");
    if (manga_search_box.style.display === "none") {
        manga_search_box.style.display = "flex";
    } else {
        manga_search_box.style.display = "none";
        }
    }


function select_manga(manga_id) {

    const selected_manga = document.getElementById(manga_id)
    const show_button  = document.getElementById("submit_button")

    if (selectedMangaId !== null) {
        const previousSelectedManga = document.getElementById(selectedMangaId);
        previousSelectedManga.style.backgroundColor = '';
        }

    selected_manga.style.backgroundColor = 'red';
    selectedMangaId = manga_id;
    show_button.style.display = "inline";
}


function search_manga() {
    var input, filter, mangaTitles, i, txtValue;
    input = document.getElementById('manga_chosen');
    filter = input.value.toLowerCase();
    mangaTitles = document.querySelectorAll(".manga_container .card li:first-of-type");

    mangaTitles.forEach(function(title) {
        txtValue = title.textContent || title.innerText;
        txtValue = txtValue.toLowerCase();
        var mangaCard = title.parentElement;
        mangaCard.style.display = (txtValue.indexOf(filter) > -1) ? "" : "none";
    });
}

async function show_results() {
    const manga_title = document.getElementById("manga_chosen").value;
    const baseUrl = 'https://api.mangadex.org';
    const search_includes = ["cover_art", "author"];

    try {
        const resp = await fetch(`${baseUrl}/manga/?title=${encodeURIComponent(manga_title)}&includes[]=${search_includes.join('&includes[]=')}`);

        if (!resp.ok) {
            throw new Error('Failed to fetch manga data');
        }

        const mangaData = await resp.json();
        console.log(mangaData);

        const displayResults = document.getElementById("displayResults");
        displayResults.innerHTML = ""; // Clear previous results

        // Limit to 5 manga covers
        mangaData.data.slice(0, 5).forEach(manga => {
            console.log(manga);
            if (manga.relationships && manga.relationships.length > 0) {
                const cover_art_filename = manga.relationships.find(relationship => relationship.type === 'cover_art')?.attributes?.fileName;
                const author = manga.relationships.find(relationship => relationship.type === 'author')?.attributes?.name;
                if (cover_art_filename) {
                    const new_div = document.createElement("div");
                    new_div.setAttribute("class","display_result_card")
                    new_div.setAttribute("id", `${manga.id}`);
                    const cover_art_url = `https://uploads.mangadex.org/covers/${manga.id}/${cover_art_filename}.256.jpg`;
                    const imgElement = document.createElement("img");
                    const author_detail = document.createElement("p")
                    imgElement.src = cover_art_url;
                    imgElement.alt = `${manga.title} cover art`;
                    author_detail.innerText = author;
                    new_div.appendChild(imgElement);
                    new_div.appendChild(author_detail)
                    new_div.addEventListener('click', () => select_manga(manga.id));
                    displayResults.appendChild(new_div);
                }
            }
        });
    } catch (error) {
        console.error('Error fetching manga data:', error);
    }
}

function setIndex(event) {
    const selected_index = document.getElementById("selected_index");

    // Get the form div
    const formDiv = document.getElementById("add_manga");

    // Clear any existing index attribute
    formDiv.removeAttribute('data-index');

    // Set the index attribute on the form div based on the target element's index
    const index = [...event.target.parentNode.parentNode.children].indexOf(event.target.parentNode);
    formDiv.setAttribute('data-index', index);

    // Set the index value in the hidden input field
    selected_index.value = index;
}