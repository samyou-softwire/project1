$("form").submit(() =>
    disable($(".should-disable"))
);

let $item = $('.item');
let $submitType = $item.find(".submittype")

function enable(element) {
    element.removeClass("disabled");
    element.removeAttr("disabled");
    element.removeAttr("readonly");
}

function disable(element) {
    element.addClass("disabled");
    element.attr("disabled", "disabled");
}

$item.find(".changestatus").click(() => {
    $submitType.attr("value", "changestatus")
})
$item.find(".submit").click(() => {
    $submitType.attr("value", "update")
})
$item.find(".delete").click(() => {
    $submitType.attr("value", "delete")
})

function edit_box(id) {
    const $task = $(`#item${id}`);

    enable($task.find(".description"))

    enable($task.find(".date"))

    const $edit = $task.find(".edit");
    $edit.addClass("d-none");

    const $submit = $task.find(".submit");
    $submit.removeClass("d-none");

    disable($item.find(".edit"))
    disable($item.find(".delete"))
    disable($item.find(".changestatus"))

    // re-enable this task's buttons
    enable($task.find(".delete"))
    enable($task.find(".changestatus"))
}

$item.find(".date").datepicker({
    format: "dd/mm/yyyy"
});