$("form").submit(() =>
    disable($(".should-disable"))
);

let $item = $('.item');

function enable(element) {
    element.removeClass("disabled");
    element.removeAttr("disabled");
}

function disable(element) {
    element.addClass("disabled");
    element.attr("disabled", "disabled");
}

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