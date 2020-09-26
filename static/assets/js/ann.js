var ans_id = 0;
var time = null;
var mydiv = document.getElementById("context");

mydiv.onmouseup = selecText;

function clearcolor(id_str) {
    for (var child of mydiv.getElementsByTagName("span")) {
        if (child.getAttribute("ansid") == id_str) {
            child.setAttribute("ansid", "0");
            child.style.color = "#000000";
        } 
    }
}

function selecText() {
    clearTimeout(time);
    time = setTimeout(function() {
        ans_id += 1;
        var userSelection = window.getSelection();
        var range = userSelection.getRangeAt(0);
        var startContainer = range.startContainer.parentElement;
        var endContainer = range.endContainer.parentElement;
        var currNode = startContainer;
        if (currNode.tagName != "DIV") {
            while (true) {
                if (currNode.getAttribute("ansid") != "0") {
                    clearcolor(currNode.getAttribute("ansid"));
                }
                currNode.setAttribute("ansid", String(ans_id));
                currNode.style.color = "red";
                
                if (currNode == endContainer) {
                    break;
                }
                currNode = currNode.nextElementSibling;
            }
        }
    }, 100);

    setTimeout(function() {
        var userSelection = window.getSelection();
        userSelection.removeAllRanges();
    }, 200);
}

mydiv.ondblclick = function() {
    clearTimeout(time);
    var userSelection = window.getSelection();
    var range = userSelection.getRangeAt(0);
    var startContainer = range.startContainer.parentElement;
    clearcolor(startContainer.getAttribute("ansid"));
}