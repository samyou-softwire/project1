$("#btn-add").mouseup(() => {
    $("#btn-add").addClass('disabled');
});

let $item = $('.item');

function edit_box(id) {
    const $task = $(`#item${id}`);

    const $description = $task.find(".description");
    $description.removeClass("disabled");
    $description.removeAttr("disabled");

    const $date = $task.find(".date");
    $date.removeClass("disabled");
    $date.removeAttr("disabled");

    const $edit = $task.find(".edit");
    $edit.addClass("d-none");

    const $submit = $task.find(".submit");
    $submit.removeClass("d-none");

    const otheredits = $item.find(".edit");
    otheredits.addClass("disabled");
    otheredits.attr("disabled", "disabled");
}

$item.find(".date").datepicker({
    format: "dd/mm/yyyy"
});