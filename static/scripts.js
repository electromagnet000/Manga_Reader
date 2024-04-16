function show_description(element_id) {
    var description_box = document.getElementById(element_id);
    if (description_box.style.display === "none") {
        description_box.style.display = "block";
    } else{
        description_box.style.display = "none";
       }
    }

