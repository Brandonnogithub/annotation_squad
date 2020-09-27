var ans_id = 0;
var time = null;
var mydiv = document.getElementById("context");
var doc_id_div = document.getElementById("docid");
var doc_id_span = document.getElementById("id_span");
var ann_count_span = document.getElementById("ann_count");

mydiv.onmouseup = selecText;

function clearcolor(id_str) {
    for (var child of mydiv.getElementsByTagName("span")) {
        if (child.getAttribute("ansid") == id_str) {
            child.setAttribute("ansid", "0");
            child.style.color = "#000000";
        } 
    }
    ann_count_span.innerHTML = Number(ann_count_span.innerHTML) - 1;
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
        var added = false;
        if (currNode.tagName != "DIV") {
            while (true) {
                if (currNode.getAttribute("ansid") != "0") {
                    clearcolor(currNode.getAttribute("ansid"));
                }
                currNode.setAttribute("ansid", String(ans_id));
                currNode.style.color = "red";
                added = true
                
                if (currNode == endContainer) {
                    break;
                }
                currNode = currNode.nextElementSibling;
            }
            if (added) {
                ann_count_span.innerHTML = Number(ann_count_span.innerHTML) + 1;
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
        total_ann.push(Number(child.getAttribute("ansid")));
    }

    return total_ann;
}


function save_page(action_, doc_id) {
    var data = {"array": getAnnData(), "action": action_, "doc_id": String(doc_id)};
    var data_str = JSON.stringify(data);
    $.ajax({
        type: 'POST',
        dataType: "json",
        url: '/savepost',
        // contentType: "application/x-www-form-urlencoded",
        data: {"data": data_str},
        success : function(return_data) {  
            var token_list = return_data["token_list"];
            var new_doc_id = return_data["doc_id"];
            var my_ann_list = return_data["ann_list"]

            doc_id_span.innerHTML = new_doc_id;
            doc_id_div.setAttribute("doc_count", new_doc_id);
            // update context
            var childs = mydiv.childNodes;
            for (var i = childs.length - 1; i >= 0; i--) {
                mydiv.removeChild(childs[i]);
            }

            var new_childs = [];
            for (var i = 0; i < token_list.length; i++) {
                new_childs.push("<span ansid='0'>"+token_list[i]+"</span>");
            }
            $("#context").append(new_childs.join("\n"));
            ans_id = 0;

            annotated_node(my_ann_list);
        } 
    });
}


function get_doc_id() {
    var doc_id = Number(doc_id_div.getAttribute("doc_count"));
    return doc_id
}


document.getElementById("previous").onclick = function() {
    save_page("previous", get_doc_id() - 1);
}

document.getElementById("next").onclick = function() {
    save_page("next", get_doc_id() + 1);
}

document.getElementById("save").onclick = function() {
    save_page("save", 0);
}

function annotated_node(ann_list) {
    var childs = mydiv.children;

    for (var i = 0; i < ann_list.length; i++) {
        ans_id += 1;
        var ann_data = ann_list[i];
        for (var j = 0; j < ann_data.length; j++) {
            childs[ann_data[j]].setAttribute("ansid", String(ans_id));
            childs[ann_data[j]].style.color = "red";
        }
    }

    // set num
    ann_count_span.innerHTML = ann_list.length;
} 
