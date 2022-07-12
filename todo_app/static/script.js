$("#btn-add").mouseup(() => {
    $("#btn-add").addClass('disabled');
});

function edit_box(id) {
    const task = $("#item62cc21a4b85ea25d99fcf2b9");

    const description = task.find(".description");
    description.removeClass("disabled");
    description.removeAttr("disabled");

    const edit = task.find(".edit");
    edit.addClass("d-none");

    const submit = task.find(".submit");
    submit.removeClass("d-none");
}