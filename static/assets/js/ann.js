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


function getAnnData() {
    var total_ann = [];

    for (var child of mydiv.getElementsByTagName("span")) {
        total_ann.push(int(child.getAttribute("ansid")));
    }

    var res = [];
    var tmp_res = [];
    
    for (var i = 0; i < total_ann.length; i++) {
        var tmp_id = total_ann[i];
        if (tmp_id != 0) {  // this one is annotated
            if (tmp_res.length == 0) {  // last one is not annotated or non exists
                tmp_res.push(i);
            }
            else {  // last one is annotated
                if (tmp_id == total_ann[tmp_res[0]]) {  // same id
                    tmp_res.push(i);
                } else {    // different id
                    res.push(tmp_res);
                    tmp_res = [i];
                }
            }
        } else {    // this one is not annotated
            if (tmp_res.length != 0) {  // last one is annotated
                res.push(tmp_res);
                tmp_res = [];
            }
        }
    }

    return total_ann;
}


function save_page(action) {
    alert("ssssss");
    var data_list = getAnnData();
    var data_str = JSON.stringify(getAnnData());
    $.ajax({
        type: 'POST',
        async: false,
        url: '/savepost',
        // contentType: "application/x-www-form-urlencoded",
        // data: {"array": data_list, "action": action},
        success : function(data) {  
            alert(data);
        } 
    });
}


document.getElementById("previous").onclick = function() {
    save_page("previous");
}

document.getElementById("next").onclick = function() {
    save_page("next");
}

document.getElementById("save").onclick = function() {
    save_page("save");
}
