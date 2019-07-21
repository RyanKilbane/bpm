function openTab(evt, details) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
        }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(details).style.display = "block";
    evt.currentTarget.className += " active";
	}

var isLockedBy = "{{ locked }}"
if (isLockedBy != ""){
    document.getElementById("saveFormButton").disabled = true;
    document.getElementById("saveFormButton").style.color = "grey";
    var bar = document.getElementById("lockedInfo");
    bar.style.display = "block";
}

document.getElementById("Form2").style.display = "block"